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
- **Before**: PSNR 28.7367, SSIM 1.0000, LPIPS 0.0374
- **Range별 After**
    - Range 0.0019 → PSNR 12.2630, SSIM 0.9931, LPIPS 0.8056  
    - Range 0.0098 → PSNR 14.1036, SSIM 0.9958, LPIPS 0.6708  
    - Range 0.0313 → PSNR 15.5869, SSIM 0.9978, LPIPS 0.4568  
    - Range 0.0430 → PSNR 16.3319, SSIM 0.9984, LPIPS 0.4271  
    - Range 0.0625 → PSNR 16.6821, SSIM 0.9986, LPIPS 0.3933  
    - Range 0.0781 → PSNR 17.0661, SSIM 0.9988, LPIPS 0.3680  
    - Range 0.0937 → PSNR 17.8029, SSIM 0.9992, LPIPS 0.3355  
    - Range 0.1250 → PSNR 18.2552, SSIM 0.9993, LPIPS 0.3149  
- **Best folder**: 0.125, PSNR 18.2552, SSIM 0.9993, LPIPS 0.3149

---

## 3. 분석 요약
1. **PSNR**: range가 증가할수록 개선되나 denoising 효과 x 
2. **SSIM**: 거의 0.99 이상으로 안정적, 구조적 손상 거의 없음
3. **LPIPS**: range 증가할수록 개선되나 denoising 효과 x 
4. **종합**: PSNR 기준 최적 range는 모두 0.125 수준, range를 더 높여서 실험해볼 것

---

## 3. Range의 의미 및 후보 선택

### 3.1 Range가 의미하는 것
- OSCAR는 latent 기반 확산 모델로, 압축된 이미지를 복원할 때 latent의 노이즈 수준을 조절합니다.  
- `range`는 latent의 distortion 또는 pseudo-noise 레벨을 의미하며, 값이 클수록 **강한 보정/재생성**을 수행합니다.

### 3.2 여러 후보를 사용하는 이유
- 압축 손상 정도가 이미지마다 다르므로, 하나의 고정된 range만 사용하면 일부 이미지는 과소 복원, 일부는 과도 복원이 발생할 수 있음  
- 여러 range 후보를 미리 계산 후 최적 값 선택 → 멀티 손상 레벨 대응  
- 일반적으로 6~10개 후보는 **계산 효율과 탐색 범위**의 균형을 고려한 값

---

## 4. Range 확장 실험 제안

| 범위 | 기대 효과 / 위험 |
|------|----------------|
| 더 큰 range (0.15, 0.2, 0.25, 0.3 …) | PSNR/SSIM/LPIPS 개선 가능성, 특히 손상 심한 이미지(JPEG10 등)에서 효과적 |
| 과도한 range | latent를 원본에서 너무 멀리 이동 → 구조 왜곡, 컬러 변화, artifact 발생 가능 |

> 참고 연구:  
> - **Noise scheduling의 중요성**: `On the Importance of Noise Scheduling for Diffusion Models`  
> - **Diffusion 기반 압축-복원 tradeoff**: `Diffusion-based Compression Quality Tradeoffs without Retraining`  
> → decoding hyper-parameter만 조정하여 PSNR과 perceptual 품질 간 trade-off 가능

---

## 5. 향후 실험 및 문서 방향

1. 기존 8개 후보 range에 더해 **0.15, 0.20, 0.25 …** 등 추가  
2. PSNR, SSIM, LPIPS 지표 + 시각적 샘플 기록  
3. 결과를 그래프로 시각화 (`range vs PSNR/LPIPS/SSIM`)  
4. qualitative 평가 + quantitative 평가 병행  
5. 최종적으로 “데이터별 최적 range 추천 값” 정리

---

### 4. 참고
- CSV 파일: `oscar_metrics_all_ranges.csv`  
- 각 row는 JPEG, range, before/after 지표, best 여부를 포함
