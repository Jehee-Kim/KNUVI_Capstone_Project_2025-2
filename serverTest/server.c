#include <dirent.h>   // 폴더 읽기용
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <fcntl.h>

#define PORT 9090           // 포트 (9090 사용 중이면 8080 등으로 바꿔도 됨)

// ★★ 여기를 네 PLY 최상위 폴더로 바꿔줘야 함 ★★
#define BASE_DIR "/Users/jehee/Documents/KNU/capstone/plyAll"

// 최대 요청 크기
#define REQ_BUF_SIZE 8192

// ---- 함수 프로토타입(선언) ----
int  get_query_value(const char *query, const char *key, char *out, size_t out_size);
void send_text_response(int client_fd, int status, const char *status_text, const char *body);
void handle_viewer_html(int client_fd);
void handle_ply(int client_fd, const char *query);
void handle_frames(int client_fd, const char *query);
void handle_client(int client_fd);

// ------------------- /frames 처리: frame 리스트 반환 -------------------
// debug.html 전송
void handle_debug_html(int client_fd) {
    const char *filename = "debug.html";
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        char msg[512];
        snprintf(msg, sizeof(msg),
                 "debug.html 파일을 찾을 수 없습니다.\n현재 디렉토리에서 실행했는지 확인하세요.");
        send_text_response(client_fd, 500, "Internal Server Error", msg);
        return;
    }

    struct stat st;
    fstat(fd, &st);
    off_t file_size = st.st_size;

    printf("[/debug] ✅ debug.html 보냄!! (%lld bytes)\n", (long long)file_size);

    char header[512];
    int hlen = snprintf(header, sizeof(header),
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "Content-Length: %lld\r\n"
                        "Connection: close\r\n"
                        "\r\n",
                        (long long)file_size);
    write(client_fd, header, hlen);

    char buf[4096];
    ssize_t n;
    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        write(client_fd, buf, n);
    }
    close(fd);
}

void handle_frames(int client_fd, const char *query) {
    char category[64] = {0};
    char codec[16]    = {0};
    char qp[64]       = {0};

    if (!get_query_value(query, "category", category, sizeof(category)) ||
        !get_query_value(query, "codec",    codec,    sizeof(codec))    ||
        !get_query_value(query, "qp",       qp,       sizeof(qp))) {

        printf("[/frames] 신호 받음 but 파라미터 부족! query=\"%s\"\n", query ? query : "(null)");
        send_text_response(client_fd, 400, "Bad Request",
                           "필수 파라미터(category, codec, qp)가 없습니다.\n");
        return;
    }

    printf("[/frames] 🔔 신호 받음! category=%s, codec=%s, qp=%s\n",
           category, codec, qp);

    char dirpath[1024];

    if (strcmp(codec, "Original") == 0) {
        snprintf(dirpath, sizeof(dirpath),
                 "%s/original/output_%s", BASE_DIR, category); // Original 처리
    } else if (strcmp(codec, "JPEG") == 0) {
        snprintf(dirpath, sizeof(dirpath),
                 "%s/JPEG/output_JPEG%s/output_%s",
                 BASE_DIR, qp, category);
    } else if (strcmp(codec, "AVC") == 0) {
        snprintf(dirpath, sizeof(dirpath),
                 "%s/AVCRA/output_AVCRA%s/output_%s",
                 BASE_DIR, qp, category);
    } else {
        printf("[/frames] 지원하지 않는 codec: %s\n", codec);
        send_text_response(client_fd, 400, "Bad Request",
                           "지원하지 않는 codec 입니다. (JPEG, AVC, Original)\n");
        return;
    }

    printf("[/frames] 디렉토리 경로: %s\n", dirpath);

    DIR *dir = opendir(dirpath);
    if (!dir) {
        printf("[/frames] 디렉토리 없음. 빈 리스트 보냄.\n");
        const char *json = "[]";
        char header[256];
        int hlen = snprintf(header, sizeof(header),
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: application/json; charset=utf-8\r\n"
                            "Content-Length: %zu\r\n"
                            "Connection: close\r\n"
                            "\r\n",
                            strlen(json));
        write(client_fd, header, hlen);
        write(client_fd, json, strlen(json));
        return;
    }

    int frames[1024];
    int count = 0;

    struct dirent *ent;
    while ((ent = readdir(dir)) != NULL) {
        const char *name = ent->d_name;
        if (name[0] == '.') continue;
        if (strncmp(name, "frame", 5) != 0) continue;
        if (strlen(name) < 11) continue;

        char numbuf[7];
        memcpy(numbuf, name + 5, 6);
        numbuf[6] = '\0';
        int f = atoi(numbuf);
        if (f < 0) continue;
        if (count < 1024) {
            frames[count++] = f;
        }
    }
    closedir(dir);

    // 정렬 (간단 버블 정렬)
    for (int i = 0; i < count; i++) {
        for (int j = i + 1; j < count; j++) {
            if (frames[i] > frames[j]) {
                int tmp = frames[i];
                frames[i] = frames[j];
                frames[j] = tmp;
            }
        }
    }

    // JSON 만들기: [1,2,3,...]
    char json[4096];
    int pos = 0;
    pos += snprintf(json + pos, sizeof(json) - pos, "[");
    for (int i = 0; i < count; i++) {
        if (i > 0) pos += snprintf(json + pos, sizeof(json) - pos, ",");
        pos += snprintf(json + pos, sizeof(json) - pos, "%d", frames[i]);
        if (pos >= (int)sizeof(json) - 10) break;
    }
    pos += snprintf(json + pos, sizeof(json) - pos, "]");
    json[sizeof(json) - 1] = '\0';

    printf("[/frames] ✅ 신호 보냄!! frame 개수=%d\n", count);

    char header[256];
    int hlen = snprintf(header, sizeof(header),
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/json; charset=utf-8\r\n"
                        "Content-Length: %zu\r\n"
                        "Connection: close\r\n"
                        "\r\n",
                        strlen(json));
    write(client_fd, header, hlen);
    write(client_fd, json, strlen(json));
}


// ------------------- 쿼리스트링 파라미터 파싱 -------------------
int get_query_value(const char *query, const char *key, char *out, size_t out_size) {
    if (!query || !key) return 0;
    size_t key_len = strlen(key);
    const char *p = query;
    while (*p) {
        const char *eq = strchr(p, '=');
        if (!eq) break;
        size_t klen = eq - p;
        if (klen == key_len && strncmp(p, key, key_len) == 0) {
            const char *val_start = eq + 1;
            const char *amp = strchr(val_start, '&');
            size_t vlen = amp ? (size_t)(amp - val_start) : strlen(val_start);
            if (vlen >= out_size) vlen = out_size - 1;
            memcpy(out, val_start, vlen);
            out[vlen] = '\0';
            return 1;
        }
        const char *amp = strchr(p, '&');
        if (!amp) break;
        p = amp + 1;
    }
    return 0;
}

// ------------------- 텍스트 응답 헬퍼 -------------------
void send_text_response(int client_fd, int status, const char *status_text, const char *body) {
    char header[512];
    size_t body_len = body ? strlen(body) : 0;
    int hlen = snprintf(header, sizeof(header),
                        "HTTP/1.1 %d %s\r\n"
                        "Content-Type: text/plain; charset=utf-8\r\n"
                        "Content-Length: %zu\r\n"
                        "Connection: close\r\n"
                        "\r\n",
                        status, status_text, body_len);
    write(client_fd, header, hlen);
    if (body_len > 0) {
        write(client_fd, body, body_len);
    }
}

// ------------------- viewer.html 전송 -------------------
void handle_viewer_html(int client_fd) {
    const char *filename = "viewer.html";
    int fd = open(filename, O_RDONLY);
    if (fd < 0) {
        char msg[512];
        snprintf(msg, sizeof(msg),
                 "viewer.html 파일을 찾을 수 없습니다.\n현재 디렉토리에서 실행했는지 확인하세요.");
        printf("[/viewer] ❌ viewer.html 못 찾음\n");
        send_text_response(client_fd, 500, "Internal Server Error", msg);
        return;
    }

    struct stat st;
    fstat(fd, &st);
    off_t file_size = st.st_size;

    printf("[/viewer] ✅ viewer.html 보냄!! (%lld bytes)\n", (long long)file_size);

    char header[512];
    int hlen = snprintf(header, sizeof(header),
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "Content-Length: %lld\r\n"
                        "Connection: close\r\n"
                        "\r\n",
                        (long long)file_size);
    write(client_fd, header, hlen);

    char buf[4096];
    ssize_t n;
    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        write(client_fd, buf, n);
    }
    close(fd);
}

// ------------------- /ply 처리 -------------------
void handle_ply(int client_fd, const char *query) {
    char category[64]  = {0};  // backpack, ball, ...
    char codec[16]     = {0};  // JPEG or AVC or Original
    char frame_str[64] = {0};  // "1" 같은 문자열
    char qp[64]        = {0};  // "10", "30", ...

    if (!get_query_value(query, "category", category, sizeof(category)) ||
        !get_query_value(query, "codec",    codec,    sizeof(codec))    ||
        !get_query_value(query, "frame",    frame_str,sizeof(frame_str))||
        !get_query_value(query, "qp",       qp,       sizeof(qp))) {

        printf("[/ply] 신호 받음 but 파라미터 부족! query=\"%s\"\n", query ? query : "(null)");
        send_text_response(client_fd, 400, "Bad Request",
                           "필수 파라미터(category, codec, frame, qp)가 없습니다.\n");
        return;
    }

    int frame_num = atoi(frame_str);
    if (frame_num < 0) {
        printf("[/ply] frame 음수: %s\n", frame_str);
        send_text_response(client_fd, 400, "Bad Request",
                           "frame은 0 이상의 숫자여야 합니다.\n");
        return;
    }

    printf("[/ply] 🔔 신호 받음! category=%s, codec=%s, frame=%d, qp=%s\n",
           category, codec, frame_num, qp);

    char frame_padded[16];
    snprintf(frame_padded, sizeof(frame_padded), "%06d", frame_num); // 000001

    char filepath[1024];

    if (strcmp(codec, "JPEG") == 0) {
        snprintf(filepath, sizeof(filepath),
                 "%s/JPEG/output_JPEG%s/output_%s/frame%s_JPEG_Q%s/points.ply",
                 BASE_DIR, qp, category, frame_padded, qp);

    } else if (strcmp(codec, "AVC") == 0) {
        snprintf(filepath, sizeof(filepath),
                 "%s/AVCRA/output_AVCRA%s/output_%s/frame%s_AVCRA_%s/points.ply",
                 BASE_DIR, qp, category, frame_padded, qp);
    } else if (strcmp(codec, "Original") == 0) {
        snprintf(filepath, sizeof(filepath),
                 "%s/original/output_%s/frame%s/points.ply", BASE_DIR, category, frame_padded); // Original 처리
    } else {
        printf("[/ply] 지원하지 않는 codec: %s\n", codec);
        send_text_response(client_fd, 400, "Bad Request",
                           "지원하지 않는 codec 입니다. (JPEG, AVC, Original)\n");
        return;
    }

    printf("[/ply] 파일 경로 후보: %s\n", filepath);

    int fd = open(filepath, O_RDONLY);
    if (fd < 0) {
        printf("[/ply] ❌ 파일 없음: %s (errno=%d)\n", filepath, errno);
        char msg[1024];
        snprintf(msg, sizeof(msg),
                 "PLY 파일을 찾을 수 없습니다:\n%s\n", filepath);
        send_text_response(client_fd, 404, "Not Found", msg);
        return;
    }

    struct stat st;
    fstat(fd, &st);
    off_t file_size = st.st_size;

    printf("[/ply] ✅ 파일 보냄!! %s (%lld bytes)\n",
           filepath, (long long)file_size);

    char header[512];
    int hlen = snprintf(header, sizeof(header),
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: application/octet-stream\r\n"
                        "Content-Length: %lld\r\n"
                        "Connection: close\r\n"
                        "\r\n",
                        (long long)file_size);
    write(client_fd, header, hlen);

    char buf[4096];
    ssize_t n;
    while ((n = read(fd, buf, sizeof(buf))) > 0) {
        write(client_fd, buf, n);
    }
    close(fd);
}

// ------------------- 클라이언트 한 명 처리 -------------------
void handle_client(int client_fd) {
    char req[REQ_BUF_SIZE];
    ssize_t n = read(client_fd, req, sizeof(req) - 1);
    if (n <= 0) {
        close(client_fd);
        return;
    }
    req[n] = '\0';

    // 첫 줄 파싱: "GET /경로 HTTP/1.1"
    char method[8], url[2048], proto[16];
    if (sscanf(req, "%7s %2047s %15s", method, url, proto) != 3) {
        send_text_response(client_fd, 400, "Bad Request", "잘못된 HTTP 요청입니다.\n");
        close(client_fd);
        return;
    }

    // url에서 path, query 분리
    char path[2048];
    char *qmark = strchr(url, '?');
    const char *query = NULL;
    if (qmark) {
        size_t plen = (size_t)(qmark - url);
        if (plen >= sizeof(path)) plen = sizeof(path) - 1;
        memcpy(path, url, plen);
        path[plen] = '\0';
        query = qmark + 1;
    } else {
        strncpy(path, url, sizeof(path) - 1);
        path[sizeof(path) - 1] = '\0';
    }

    printf("== [handle_client] 요청 받음: %s %s (query=%s)\n",
           method, path, query ? query : "(none)");

    // GET만 지원
    if (strcmp(method, "GET") != 0) {
        send_text_response(client_fd, 405, "Method Not Allowed", "GET만 지원합니다.\n");
        close(client_fd);
        return;
    }

    // 라우팅
    if (strcmp(path, "/") == 0 || strcmp(path, "/viewer.html") == 0 || strcmp(path, "/viewer") == 0) {
        handle_viewer_html(client_fd);
    } else if (strcmp(path, "/ply") == 0) {
        handle_ply(client_fd, query);
    } else if (strcmp(path, "/frames") == 0) {
        handle_frames(client_fd, query);
    } else if (strcmp(path, "/debug.html") == 0) {
        handle_debug_html(client_fd); 
    } else {
        printf("[handle_client] 알 수 없는 path: %s\n", path);
        send_text_response(client_fd, 404, "Not Found", "지원하지 않는 경로입니다.\n");
    }

    close(client_fd);
}
// ------------------- main -------------------
int main(void) {
    // stdout 버퍼 비움 (printf가 바로바로 찍히게)
    setvbuf(stdout, NULL, _IONBF, 0);

    // 서버 소켓 생성
    int server_fd = socket(AF_INET, SOCK_STREAM, 0);
    if (server_fd < 0) {
        perror("socket");
        exit(1);
    }

    // 소켓 옵션 설정 (재사용 주소)
    int opt = 1;
    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    // 서버 주소 설정
    struct sockaddr_in addr;
    memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);  // 지정된 포트
    addr.sin_addr.s_addr = htonl(INADDR_ANY);  // 모든 IP에서 연결 허용

    // 바인드(bind) 호출
    if (bind(server_fd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("bind");
        close(server_fd);
        exit(1);
    }

    // 클라이언트 연결 대기
    if (listen(server_fd, 16) < 0) {
        perror("listen");
        close(server_fd);
        exit(1);
    }

    printf("서버 시작: http://localhost:%d/viewer.html\n", PORT);

    // 무한 루프: 클라이언트 요청 대기
    while (1) {
        // 클라이언트 연결 수락
        struct sockaddr_in client_addr;
        socklen_t client_len = sizeof(client_addr);
        int client_fd = accept(server_fd, (struct sockaddr *)&client_addr, &client_len);
        if (client_fd < 0) {
            perror("accept");
            continue;
        }

        // 클라이언트 요청 처리
        handle_client(client_fd);
    }

    // 서버 종료 시 소켓 닫기
    close(server_fd);
    return 0;
}
