## 주제 : 멀티뷰 비디오 및 이미지 압축에 대한 3DGS 성능비교 케이스 스터디

### 기술 스택 및 데이터셋

주요 기술 : 3D Gaussian Splatting (3DGS)

개발 언어 : Python

데이터셋 : Mip-NeRF360의 9가지 장면 사용

### 연구 방법론 및 진행 상황

**HEVC  압축 단계**

**전처리 :**

- 이미지 해상도 8배 다운스케일링 진행
- 영상 프레임이 아닌 3개의 카테고리 (bicycle, flowers, treehill)에 대해 각 장면의 원본 이미지를 시간 순으로 정렬하여 프레임 시퀀스를 생성
- ffmpeg을 사용하여 해상도 홀수를 짝수로 맞추는 crop 수행
- YUV444p 포맷(raw video)으로 변환

**압축 :**

- ffmpeg을 사용해 다운스케일링된 이미지 시퀀스를 yuv444p 비디오로 변환
- HM(HEVC Test Model)의 encoder_randomaccess_main.cfg를 사용해 Random Access 모드(GOP 기반)로 인코딩
I/P/B 프레임 구조를 사용하여 프레임 간 예측(inter prediction)까지 포함
- Quantization Parameter (QP) 값을 27, 32, 37, 42으로 설정
QP 값이 낮을수록 화질이 좋고 압축률이 낮으며, 높을수록 압축률이 높아짐

**3DGS 모델 학습 :**

- HEVC 비디오에서 ffmpeg으로 다시 PNG 시퀀스로 디코딩
- 추출된 이미지 시퀀스로 COLMAP을 통해 카메라 포즈 및 sparse point cloud를 추정하여 cameras.bin, images.bin, points3D.bin 파일 생성
- 생성된 BIN 파일을 기반으로 모든 카테고리에 대해 3DGS 모델 학습 및 렌더링 완료, 현재  PSNR, SSIM, LPIPS를 사용해 정량평가 진행 중

**JPEG 압축 단계**

**전처리 :**

- 이미지 해상도 8배 다운스케일링 진행

**압축 :** 

- JPEG 코덱으로 압축 진행
- Quality Factor (QF) 값을 10, 30, 50, 70, 90으로 설정
QF 값이 낮을수록 압축률이 높고 화질이 떨어지며, 높을수록 압축률이 낮고 화질이 좋아짐

**3DGS 모델 학습: (위와 동일)**

- 압축된 JPEG 이미지들을 사용하여 COLMAP으로 BIN 파일을 생성
- 생성된 BIN 파일을 기반으로 모든 카테고리에 대해 3DGS 모델을 학습 및 렌더링 완료

### 성능 비교 및 결과 분석 (예정)

**평가 지표 :**

- **PSNR (Peak Signal-to-Noise Ratio)**: 원본 이미지와 렌더링된 이미지의 픽셀 단위 차이를 측정하는 지표로, 수치가 높을수록 좋다
- **SSIM (Structural Similarity Index)**: 이미지의 밝기, 대비, 구조적 정보를 고려하여 유사도를 측정하는 지표로, 1에 가까울수록 좋다
- **LPIPS (Learned Perceptual Image Patch Similarity)**: 딥러닝 모델을 사용하여 인간의 시각적 인지 특성을 반영해 이미지 유사도를 측정하는 지표로, 수치가 낮을수록 좋다

**분석 계획 :** 

- 각 압축 방식(HEVC, JPEG)의 QP 및 QF 값 변화에 따른 3DGS 렌더링 결과의 PSNR, SSIM, LPIPS 값 변화를 그래프로 시각화하여 비교할 예정
- 코덱 대비, 압축률 대비 3D 재구성 성능의 trade-off 관계를 분석하여 결론을 도출해 논문 작성
