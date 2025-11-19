# 이미지/비디오 통합 압축 파이프라인 (Image/Video Integrated Compression Pipeline)

## 개요 (Overview)

이 프로젝트는 이미지 및 비디오 압축을 자동화하기 위한 커맨드 라인 인터페이스(CLI) 파이프라인을 제공합니다. 사용자는 통합된 하나의 명령어를 통해 다양한 미디어 파일을 여러 코덱과 품질 설정으로 손쉽게 인코딩할 수 있습니다. 이 파이프라인은 모듈식으로 설계되어 각 코덱에 특화된 스크립트를 호출하여 작업을 수행합니다.

## 주요 기능 (Features)

- **통합 인터페이스**: `main.py` 스크립트 하나로 모든 작업을 제어합니다.
- **다중 코덱 지원**: **HEVC** (High Efficiency Video Coding), **AVC** (H.264), 그리고 **JPEG** (일반 이미지)를 지원합니다.
- **유연한 입력 처리**: 단일 파일뿐만 아니라 디렉토리 내의 모든 지원 파일을 일괄 처리할 수 있습니다.
- **품질 제어**: `--QP` 인자를 사용하여 원하는 품질 수준을 쉽게 설정할 수 있습니다.
- **경로 설정 가능**: HEVC 인코더의 실행 경로를 명령줄 인자로 지정할 수 있어 하드코딩된 경로 문제에서 자유롭습니다.
- **상세한 로깅**: 압축 진행 상황에 대한 명확한 실시간 피드백을 제공합니다.

## 사전 요구사항 (Prerequisites)

파이프라인을 실행하기 전에 다음 요구사항이 충족되었는지 확인해 주세요.

1.  **Python 3**: 메인 스크립트와 JPEG 인코더는 Python 3로 작성되었습니다.
2.  **FFmpeg**: **AVC (H.264)** 인코딩을 위해 필요합니다. 시스템에 설치되어 있고 PATH에 등록되어 있어야 합니다.
3.  **Pillow 라이브러리**: JPEG 스크립트는 Pillow 라이브러리를 사용합니다. pip를 통해 설치하세요:
    ```bash
    pip install Pillow
    ```
4.  **스크립트 실행 권한**: 셸 스크립트들에 실행 권한이 필요합니다. `chmod`를 사용하여 권한을 부여하세요:
    ```bash
    chmod +x Code/for/CompressionSW/*.sh
    ```
5.  **HEVC 인코더**: HEVC 인코딩을 위해서는 HEVC 인코더 실행 파일(예: HM 참조 소프트웨어의 `TAppEncoder`)이 필요합니다. 실행 시 해당 파일의 경로를 제공해야 합니다.

## 사용법 (Usage)

모든 작업은 `main.py` 스크립트를 통해 시작됩니다.

### 기본 명령어 구조

```bash
python3 Code/for/CompressionSW/main.py --codec <CODEC> --QP <VALUE> --input <PATH> --output <PATH> [OPTIONS]
```

### 실행 예시 (Examples)

**1. HEVC 인코딩**

Raw YUV 비디오 파일을 인코딩합니다. `--width`와 `--height` 인자는 **필수**입니다.

```bash
# QP 27로 1920x1080 YUV 파일 인코딩
python3 Code/for/CompressionSW/main.py \
    --codec HEVC \
    --QP 27 \
    --input /path/to/video.yuv \
    --output ./hevc_results \
    --width 1920 \
    --height 1080 \
    --encoder_path /path/to/your/TAppEncoder
```

**2. AVC (H.264) 인코딩**

FFmpeg를 사용하여 비디오 파일을 인코딩합니다. Raw YUV 파일과 일반 비디오 포맷(mp4, avi 등)을 모두 지원합니다.

```bash
# 일반 비디오 파일(mp4, avi 등)을 QP 30으로 인코딩
python3 Code/for/CompressionSW/main.py \
    --codec AVC \
    --QP 30 \
    --input /path/to/video.mp4 \
    --output ./avc_results

# Raw YUV 파일을 인코딩 (해상도 정보 필수)
python3 Code/for/CompressionSW/main.py \
    --codec AVC \
    --QP 30 \
    --input /path/to/raw_video.yuv \
    --output ./avc_results \
    --width 1920 \
    --height 1080
```

**3. JPEG 압축**

일반 이미지 파일(PNG, BMP 등)을 JPEG 포맷으로 압축합니다.

```bash
# 품질(Quality) 90으로 이미지 압축
python3 Code/for/CompressionSW/main.py \
    --codec JPEG \
    --QP 90 \
    --input /path/to/image.png \
    --output ./jpeg_results
```

## 인자 설명 (Argument Reference)

- `--codec`: 사용할 코덱 (`HEVC`, `AVC`, `JPEG`).
- `--QP`: 품질/양자화 파라미터 (Quantization Parameter).
  - **HEVC/AVC**: 양자화 파라미터 (값이 **낮을수록** 고화질).
  - **JPEG**: 품질 점수 (값이 **높을수록** 고화질, 1-95 권장).
- `--input`: 입력 파일 또는 디렉토리 경로.
- `--output`: 결과물을 저장할 디렉토리 경로.
- `--width`: 입력 비디오의 가로 해상도. **HEVC 및 AVC(YUV 입력 시) 필수.**
- `--height`: 입력 비디오의 세로 해상도. **HEVC 및 AVC(YUV 입력 시) 필수.**
- `--encoder_path`: (선택 사항) HEVC 인코더 실행 파일의 경로.

## 스크립트 개요 (Scripts Overview)

- `main.py`: 메인 컨트롤러입니다. 사용자 인자를 파싱하고 적절한 스크립트를 호출합니다.
- `encode_hevc_single.sh`: HEVC 인코더(HM)를 사용하여 단일 YUV 파일을 인코딩합니다.
- `encode_avc_single.sh`: FFmpeg를 사용하여 단일 파일을 AVC(H.264)로 인코딩합니다.
- `encode_jpeg_single.py`: Pillow를 사용하여 단일 이미지 파일을 JPEG로 압축합니다.
