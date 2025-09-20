# Evaluation metric 조사

## AUC@30
- 30도 임계값에서의 Area Under Curve
    - RRA : Relative Rotation Accuracy
    - RTA : Relative Translation Accuracy
    - AUC : RRA, RTA 중 작은 값을 기준으로 하는 면적?? 이해 못했음... 아마 카메라포즈 관련 메트릭인듯

## Chamfer Distance
: 두 점 집합 사이의 유사성이나 차이를 측정하는 메트릭.
- Accuracy : 예측된 3D point들에 대해, 가장 가까운 GT point와의 유클리드 거리
- Completeness : GT point들에 대해, 가장 가까운 예측된 3D point와의 유클리드 거리
- Chamfer Distance : 위 둘의 평균

**장점**
- outlier에 민감하지만, 다루기 쉬워 자주 사용됨
- 계산을 효율적으로 할 수 있음 (n^2 시간복잡도)
    - 최근에는 KD-Tree, 중요도 샘플링이나 근사 알고리즘 등을 통해 nlogn까지 줄일 수 있음이 입증됨
    - 주요 ML 프레임워크에 내장되어 있어 GPU 활용 병렬처리가 쉬움
- 미분 가능하기 때문에 딥러닝 loss로 활용하기 적합함

+ 정량평가 진행한 뒤, 3D downstream tasks(Object Detection 등)을 이용한 추가 평가도 진행할 예정

### 주의사항
- 우리가 사용하는 데이터셋 GT에는 배경 포인트가 없기 때문에, 아웃풋에서 배경을 마스킹할 수 있는 방법을 찾아야 함. (SAM 등)

### SAM 관련 조사
- SAM은 2D 이미지 마스킹 모델 → 같은 원리로 개발한 Point-SAM, SAM3D 등을 사용해야 함


## LPIPS, SSIM, PSNR
3D scene의 렌더링 결과를 비교하는 방법으로는
→ LPIPS, SSIM, PSNR

### **LPIPS :** Learned Perceptual Image Patch Similarity
- 딥러닝 기반 이미지 유사성 평가 지표 : 수치가 작을수록 유사함
- CNN을 사용해 추출한 특징 맵을 비교하여 지각적 유사도 평가

### **SSIM :** Structural Similarity Index Measure
- 구조, 명암 대비와 같은 구조적 정보를 비교하여 유사도 평가

### **PSNR :** Peak Signal-to-Noise Ratio
- 픽셀값 차이를 기반으로 원본과 오차의 비율을 dB 단위로 측정
- 값이 클수록 유사함
- 계산이 매우 간단함