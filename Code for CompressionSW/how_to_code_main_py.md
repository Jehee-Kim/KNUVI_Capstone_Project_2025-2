# `main.py` 최종 개발 가이드

이 문서는 `main.py`를 중심으로 한 압축 파이프라인의 최종 설계와 구현에 대해 설명합니다. 초기 아이디어를 발전시켜 완성된 코드의 작동 방식을 상세히 기술합니다.

### 1. 최종 기능 명세

완성된 파이프라인은 다음 기능을 포함합니다.

- **통합된 CLI**: `main.py`를 통해 `HEVC`, `JPEG` 압축을 모두 제어합니다.
- **유연한 인자 처리**:
  - `HEVC` 코덱을 위한 `--width`, `--height` 인자를 지원합니다.
  - `HEVC` 인코더 경로를 지정할 수 있는 `--encoder_path` 옵션을 제공합니다.
- **모듈화된 스크립트 호출**:
  - 각 코덱별로 특화된 단일 파일 처리용 스크립트(`encode_hevc_single.sh`, `encode_jpeg_single.py`)를 호출합니다.
  - 셸 스크립트와 Python 스크립트를 구분하여 올바른 방식으로 실행합니다.
- **견고한 입력 처리**: 단일 파일뿐만 아니라 디렉토리 전체를 입력으로 받아 처리할 수 있습니다.
- **상세 로깅**: `logging` 모듈을 사용하여 모든 처리 과정을 체계적으로 기록합니다.

### 2. `main.py` 핵심 로직 상세

#### 2.1. 확장된 인자 파싱 (`argparse`)

`HEVC` 코덱에 특화된 인자와 경로 지정을 위한 인자가 추가되었습니다.

```python
# main() 함수 내부
parser = argparse.ArgumentParser(description="Integrated Image/Video Compression Pipeline Software")

# ... 기본 인자들 ...
parser.add_argument("--codec", required=True, help="Codec to use (e.g., HEVC, JPEG)")
parser.add_argument("--QP", required=True, type=int, help="Quantization Parameter or JPEG Quality")
# ...

# HEVC 전용 인자 추가
parser.add_argument("--width", type=int, help="Frame width (required for HEVC codec)")
parser.add_argument("--height", type=int, help="Frame height (required for HEVC codec)")

# HEVC 인코더 경로를 위한 선택적 인자 추가
parser.add_argument("--encoder_path", help="Path to the HEVC encoder executable (e.g., TAppEncoder)")
```

#### 2.2. 코덱별 스크립트 분기 (`get_script_path`)

기존 배치 스크립트 대신, 새로 작성된 단일 파일 처리용 스크립트를 가리키도록 수정되었습니다.

```python
def get_script_path(codec):
    """Returns the path to the corresponding script for the given codec."""
    if codec.upper() == "HEVC":
        return "./encode_hevc_single.sh"  # HEVC 단일 처리용 스크립트
    elif codec.upper() == "JPEG":
        return "./encode_jpeg_single.py"  # JPEG 단일 처리용 스크립트
    else:
        return None
```

#### 2.3. 동적 명령어 생성 로직

`main.py`의 가장 핵심적인 부분으로, 코덱 종류에 따라 실행할 명령어를 동적으로 생성합니다.

```python
# main() 함수 내부, 파일 처리 루프
for file_path in files_to_process:
    # ...
    is_python_script = script_path.endswith('.py')
    command = []

    if is_python_script:
        # Python 스크립트(JPEG)를 위한 명령어 생성
        command = [
            "python3", script_path,
            "--quality", str(args.QP),  # --QP를 --quality로 전달
            "--input", file_path,
            "--output", output_file_path
        ]
    else:
        # 셸 스크립트(HEVC)를 위한 명령어 생성
        command = [
            script_path,
            "--qp", str(args.QP),
            "--input", file_path,
            "--output", output_file_path
        ]
        # HEVC 전용 인자들을 조건부로 추가
        if args.codec.upper() == "HEVC":
            command.extend(["--width", str(args.width), "--height", str(args.height)])
            if args.encoder_path:
                command.extend(["--encoder_path", args.encoder_path])

    run_command(command)
```
- **스크립트 타입 확인**: `.py` 확장자로 Python 스크립트인지 셸 스크립트인지 확인합니다.
- **Python 스크립트 호출**: `python3` 인터프리터를 명령어에 추가하고, `--QP` 값을 `--quality` 인자로 전달합니다.
- **셸 스크립트 호출**: `--QP` 값을 `--qp` 인자로 전달하고, `HEVC` 코덱일 경우 `--width`, `--height`, `--encoder_path` 인자를 동적으로 추가합니다.

### 3. 헬퍼 스크립트 설계

`main.py`의 모듈식 설계를 뒷받침하기 위해, 기존 배치 스크립트들을 대체하는 새로운 헬퍼 스크립트들이 작성되었습니다.

- **`encode_hevc_single.sh`**:
  - `main.py`로부터 `--qp`, `--input`, `--output`, `--width`, `--height`, `--encoder_path` 인자를 받아 단일 YUV 파일을 인코딩합니다.
  - 인코더 경로가 주어지지 않으면 내장된 기본 경로를 사용합니다.

- **`encode_jpeg_single.py`**:
  - `main.py`로부터 `--quality`, `--input`, `--output` 인자를 받아 단일 이미지 파일을 JPEG로 압축합니다.
  - `Pillow` 라이브러리를 사용하여 다양한 이미지 입력을 처리합니다.

### 4. 최종 실행 예시

이러한 설계를 통해, 사용자는 다음과 같이 명확하고 유연한 명령어로 파이프라인을 실행할 수 있습니다.

**HEVC 인코딩 (인코더 경로 지정):**
```bash
python3 Code/for/CompressionSW/main.py \
    --codec HEVC \
    --QP 27 \
    --input /path/to/video.yuv \
    --output ./hevc_results \
    --width 1920 \
    --height 1080 \
    --encoder_path /path/to/my/TAppEncoder
```

**JPEG 압축:**
```bash
python3 Code/for/CompressionSW/main.py \
    --codec JPEG \
    --QP 90 \
    --input /path/to/image.png \
    --output ./jpeg_results
```

### 5. 향후 확장 계획: AV1 코덱 추가

현재의 모듈식 설계 덕분에 새로운 코덱을 추가하는 작업이 용이합니다. 향후 AV1 코덱을 지원하려면 다음과 같은 단계로 파이프라인을 확장할 수 있습니다.

1.  **AV1 인코더 헬퍼 스크립트 생성 (`encode_av1_single.sh` 등)**
    -   `aomenc` 또는 `svt-av1`과 같은 실제 AV1 인코더를 감싸는 래퍼(wrapper) 스크립트를 작성합니다.
    -   이 스크립트는 `main.py`로부터 `--input`, `--output`, `--qp` 등 압축에 필요한 인자들을 커맨드 라인으로 받아 처리해야 합니다.

2.  **`main.py` 업데이트**
    -   `get_script_path` 함수에 `AV1` 코덱을 위한 분기를 추가하여, 위에서 생성한 `encode_av1_single.sh` 스크립트를 반환하도록 설정합니다.
    -   `main` 함수의 명령어 생성 로직에 `AV1` 코덱을 위한 조건부를 추가합니다. 만약 AV1 인코딩에만 필요한 특별한 인자(예: `--cpu-used`, `--tile-columns` 등)가 있다면, `argparse`에 해당 인자를 추가하고 명령어 생성 시 동적으로 포함시킵니다.
