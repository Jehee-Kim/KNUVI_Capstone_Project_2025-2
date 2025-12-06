# OSCAR JPEG 복원 결과 분석

이 문서에서는 **OSCAR**를 사용한 JPEG 압축 이미지 복원 실험 결과를 정리합니다.  
실험에서는 JPEG10, JPEG50, JPEG70 등 서로 다른 압축률 이미지를 대상으로, 다양한 **range 파라미터**를 적용해 PSNR, SSIM, LPIPS 지표를 측정했습니다.

## 1. 실험 환경
- **모델**: OSCAR (Stable Diffusion 기반)
- **평가 지표**
  - PSNR: Peak Signal-to-Noise Ratio (높을수록 원본에 가까움)
  - SSIM: Structural Similarity Index (1에 가까울수록 원본과 구조 유사)
  - LPIPS: Learned Perceptual Image Patch Similarity (낮을수록 원본과 시각적 유사)

---

## 2. 전체 결과

### JPEG10
- **Before**: PSNR 22.6170, SSIM 0.9998, LPIPS 0.3334
- **Range별 After**
    - Range 0.0019 → PSNR 12.5056, SSIM 0.9935, LPIPS 0.8459  
    - Range 0.0098 → PSNR 14.3914, SSIM 0.9962, LPIPS 0.7498  
    - Range 0.0313 → PSNR 15.7187, SSIM 0.9978, LPIPS 0.5676  
    - Range 0.0430 → PSNR 16.4308, SSIM 0.9984, LPIPS 0.5487  
    - Range 0.0625 → PSNR 16.5166, SSIM 0.9984, LPIPS 0.5502  
    - Range 0.0781 → PSNR 17.2520, SSIM 0.9988, LPIPS 0.5104  
    - Range 0.0937 → PSNR 17.8544, SSIM 0.9992, LPIPS 0.5006  
    - Range 0.1250 → PSNR 18.2837, SSIM 0.9993, LPIPS 0.4854  
- **Best folder**: 0.125, PSNR 18.2837, SSIM 0.9993, LPIPS 0.4854

### JPEG50
- **Before**: PSNR 26.9773, SSIM 1.0000, LPIPS 0.0707
- **Range별 After**
    - Range 0.0019 → PSNR 12.2537, SSIM 0.9931, LPIPS 0.8117  
    - Range 0.0098 → PSNR 14.1237, SSIM 0.9959, LPIPS 0.6821  
    - Range 0.0313 → PSNR 15.6053, SSIM 0.9978, LPIPS 0.4703  
    - Range 0.0430 → PSNR 16.3470, SSIM 0.9984, LPIPS 0.4390  
    - Range 0.0625 → PSNR 16.6829, SSIM 0.9986, LPIPS 0.4030  
    - Range 0.0781 → PSNR 17.0987, SSIM 0.9988, LPIPS 0.3783  
    - Range 0.0937 → PSNR 17.8309, SSIM 0.9992, LPIPS 0.3453  
    - Range 0.1250 → PSNR 18.3174, SSIM 0.9993, LPIPS 0.3256  
- **Best folder**: 0.125, PSNR 18.3174, SSIM 0.9993, LPIPS 0.3256

### JPEG70
- **Before**:험
2. PSNR, SSIM, LPIPS 지표 + 시각적 샘플 기록  
3. 결과를 그래프로 시각화 (`range vs PSNR/LPIPS/SSIM`)  
4. qualitative 평가 + quantitative 평가 병행  
5. 최종적으로 “데이터별 최적 range 추천 값” 정리

---

### 7. 참고
- CSV 파일: `oscar_metrics_all_ranges.csv`  
- 각 row는 JPEG, range, before/after 지표, best 여부를 포함
