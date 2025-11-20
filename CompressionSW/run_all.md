# Dataset Compression Pipeline

### *JPEG / HEVC (HM 18.0) 기반 데이터셋 자동 압축 스크립트*

이 프로젝트는 Neural Radiance Fields(NeRF), 3D Gaussian Splatting(3DGS) 등

이미지 기반 3D 비전 모델에서 **입력 이미지의 압축 수준이 성능에 미치는 영향**을 분석하기 위한 자동 압축 파이프라인입니다.

이 스크립트는 다음 두 가지 압축 방식을 지원합니다:

- **JPEG 압축** (ImageMagick `convert`)
- **HEVC 압축** (HEVC Reference Software **HM 18.0**, RandomAccess 모드)

사용자는 `hevc`, `jpeg` 중 원하는 방식을 선택해 실행할 수 있으며,

여러 Quality(Q) 또는 QP 값을 한 번에 입력할 수 있습니다.

---

# 실행 방법

```bash
./run_all.sh

```


스크립트 실행 시 다음을 입력합니다:

데이터셋 경로
예: /mnt/c/Users/user/Desktop/dataset

코덱 선택: hevc 또는 jpeg

QP 또는 JPEG 품질 값 리스트
예: 10 30 50 70 90

# 폴더 구조

```
dataset/
 ├─ frames/              # 원본 프레임 (각 scene 폴더 안에 frame_000001.JPG ...)
 │   ├─ bicycle/
 │   ├─ bonsai/
 │   └─ ...
 │
 ├─ jpeg_output/         # JPEG 압축 결과
 │
 ├─ yuv/                 # JPG → YUV 변환 중간 파일
 ├─ bitstream/           # HEVC 인코딩 *.bin output
 ├─ recon/               # HEVC 복원된 *.yuv
 ├─ coding_log/          # 인코딩 로그
 │
 ├─ <QP>/                # HEVC decoding 이미지 (png 추출)
 │    └─ 1_bicycle/
 │        └─ images/
 │            └─ img_000001.png

```

---

# JPEG 압축

ImageMagick의 `convert`를 사용하여 다음 명령 형태로 실행됩니다:

```
convert input.jpg -quality <Q> output.jpg

```

scene × quality × image 단위로 자동 압축됩니다.

---

# HEVC 압축

파일 이름 정리:
_DSC*, DSC*, DSCF*로 시작하는 모든 이미지 파일을 img_000001.jpg 형식으로 일괄 변경합니다.

JPG → YUV 변환:
FFmpeg를 사용하여 이미지 시퀀스를 YUV 4:4:4 형식으로 변환합니다.
결과는 yuv/<scene>.yuv로 저장됩니다.

HEVC 인코딩:

각 씬별 YUV 파일을 HM 18.0을 사용하여 HEVC로 인코딩

QP 리스트에 따라 비트스트림 생성 (bitstream/<scene>_qp<q>.bin)

재구성 파일도 동시에 생성 (recon/<scene>_qp<q>.yuv)

병렬 처리: 시스템 CPU 코어 수만큼 동시에 인코딩 실행

YUV → PNG 변환:
재구성된 YUV 파일을 PNG 시퀀스로 변환하여 각 씬별 폴더에 저장 (<qp>/<scene>/images/)

다음 설정을 반드시 cfg 파일에 적용해야 합니다:

```
Profile = main-RExt
InputChromaFormat = 444
ConformanceWindowMode = 1

```

이 설정 중 하나라도 빠지면 4:4:4 YUV 입력이 정상적으로 인코딩되지 않으며,

특히 `ConformanceWindowMode=1`을 설정하지 않으면 chroma alignment 오류가 발생합니다.

# 스크립트 구조 요약

```
encode.sh
├─ 사용자 입력
│  ├─ base_root (데이터셋 경로)
│  ├─ codec 선택 (hevc / jpeg)
│  └─ QP / Quality 리스트
├─ jpeg_compress()  // JPEG 압축
├─ hevc_encode()    // HEVC 인코딩
│   ├─ 파일 이름 정리 (_DSC / DSC / DSCF → img_000001)
│   ├─ JPG → YUV 변환 (yuv444p)
│   ├─ HEVC 인코딩 (HM 18.0, cfg 적용)
│   └─ YUV → PNG 변환
└─ 사용자 선택에 따라 실행
```

# 주의 사항

HM 인코더(TAppEncoder)는 cfg 설정에 따라 동작하므로, 반드시 Profile, Chroma Format, ConformanceWindowMode를 확인하세요.

YUV 변환 전 반드시 이미지 파일 이름을 정리해야 FFmpeg가 순차적으로 읽을 수 있습니다.

스크립트는 병렬 인코딩을 지원하지만, 코어 수가 많을수록 메모리 사용량도 증가합니다.
