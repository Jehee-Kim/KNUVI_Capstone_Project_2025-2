
# KNUVI Capstone Project 2025-2
**경북대학교 (KNU) - 시각 지능 (KNUVI) 캡스톤 프로젝트**

## 📋 프로젝트 개요

본 프로젝트는 **3D Gaussian Splatting (3DGS)** 및 **Visual Geometry Grounded Transformer (VGGT)** 기술을 활용한 3D 재구성 및 성능 분석 연구입니다. Structure-from-Motion (SfM) 파이프라인과 최신 딥러닝 기반 3D 재구성 기술을 비교·분석하고, 성능 개선 방법론을 제시합니다.

### 주요 목표
- 3DGS와 VGGT를 활용한 고품질 3D 재구성
- COLMAP 기반 SfM 파이프라인 자동화 및 최적화
- 정량적 평가 지표(PSNR, SSIM, LPIPS, Chamfer Distance) 기반 성능 분석
- 코덱 압축 및 전처리 기법을 통한 성능 향상 연구

---

## 🎯 주요 기능

### 1. **3D Gaussian Splatting (3DGS)**
- 실시간 렌더링 가능한 3D 장면 재구성
- Anisotropic Gaussian 기반 최적화
- 고품질 시각적 재구성 결과 생성

### 2. **Visual Geometry Grounded Transformer (VGGT)**
- Feed-forward 방식의 빠른 3D 재구성
- 단일 이미지 또는 다중 이미지 입력 지원
- 카메라 파라미터, 깊이 맵, 포인트 클라우드 직접 추론

### 3. **COLMAP 자동화**
- Structure-from-Motion (SfM) 파이프라인 자동화
- Feature 추출 및 매칭 안정화
- Outlier 제거 및 최적화 기능

### 4. **성능 평가**
- **정량적 지표**: PSNR, SSIM, LPIPS, Chamfer Distance
- 시각화 도구를 통한 결과 분석
- 다양한 데이터셋에 대한 벤치마킹

---

## 🗂 프로젝트 구조

```
KNUVI_Capstone_Project_2025-2/
├── 3DGS_RESULT/                  # 3D Gaussian Splatting 결과물
├── VGGT_RESULT/                  # VGGT 재구성 결과물
├── Performance_Analysis/         # 성능 분석 코드 및 문서
│   ├── 3DGS_Paper.md            # 3DGS 논문 요약
│   ├── vggt.md                  # VGGT 관련 문서
│   ├── chamfer_distance.py      # Chamfer Distance 계산
│   ├── psnr_ssim_lpipls_score.py # PSNR, SSIM, LPIPS 계산
│   ├── colmap_auto.py           # COLMAP 자동화 스크립트
│   ├── colmap_upgrade.py        # COLMAP 개선 버전
│   ├── analyze_colmap.py        # COLMAP 결과 분석
│   ├── outlier_removal.sh       # Outlier 제거 스크립트
│   ├── evaluation_metrics.md    # 평가 지표 문서
│   └── 3DGS_setting/            # 3DGS 실험 설정 로그
├── Performance_improving/        # 성능 개선 연구
├── CodecCode/                    # 코덱 압축 코드
├── Meeting Note/                 # 멘토 미팅 기록
├── Others/                       # 발표자료 및 기타 문서
│   ├── Plan_presentation/       # 계획 발표
│   ├── Midterm_Presentation_1_Requirement_Analysis/
│   ├── Midterm_presentation_3/  # 중간발표 자료
│   ├── Progress_VGGT/           # VGGT 진행 상황
│   ├── ply_test/                # PLY 파일 처리 테스트
│   ├── Dataset정리_0910.xlsx    # 데이터셋 조사
│   └── Gantt_chart_1008.xlsx    # 프로젝트 일정표
├── matric/                       # 평가 메트릭 유틸리티
└── images/                       # 구조도 및 이미지 자료
```

---

## 🛠 설치 및 환경 설정

### 요구사항
- Python 3.8+
- CUDA 11.3+ (GPU 필수)
- PyTorch 2.0+
- COLMAP 3.8+


## 🚀 사용 방법

### 1. COLMAP 자동화 실행
```
python Performance_Analysis/colmap_auto.py --input_path <이미지_폴더> --output_path <출력_폴더>
```

### 2. 3DGS 학습 및 재구성
```
# 3DGS 공식 저장소 활용
# https://github.com/graphdeco-inria/gaussian-splatting
```

### 3. 성능 평가
```
# PSNR, SSIM, LPIPS 계산
python Performance_Analysis/psnr_ssim_lpipls_score.py --gt_dir <GT경로> --pred_dir <예측경로>

# Chamfer Distance 계산
python Performance_Analysis/chamfer_distance.py --source <소스.ply> --target <타겟.ply>
```

### 4. 결과 시각화
```
python Performance_Analysis/visulization_for_chamfer_distance.py --input <입력.ply>
```

---

## 📊 평가 지표

본 프로젝트에서 사용하는 주요 평가 지표:

| 지표 | 설명 | 용도 |
|------|------|------|
| **PSNR** | Peak Signal-to-Noise Ratio | 이미지 품질 평가 |
| **SSIM** | Structural Similarity Index | 구조적 유사도 측정 |
| **LPIPS** | Learned Perceptual Image Patch Similarity | 지각적 유사도 평가 |
| **Chamfer Distance** | Point Cloud Distance | 3D 기하학적 정확도 |

자세한 설명은 [`Performance_Analysis/evaluation_metrics.md`](Performance_Analysis/evaluation_metrics.md)를 참조하세요.

---

## 📈 실험 결과

### 3DGS 결과
- 실시간 렌더링 성능 달성
- PSNR: XX.XX dB
- SSIM: 0.XXX
- 상세 결과: [`3DGS_RESULT/`](3DGS_RESULT/)

### VGGT 결과
- Feed-forward 추론 시간: < 1초
- 다중 이미지 재구성 성능 검증
- 상세 결과: [`VGGT_RESULT/`](VGGT_RESULT/)

### 성능 비교
발표 자료 및 분석 결과는 [`Others/`](Others/) 폴더를 참조하세요.

---

## 👥 팀원

- **이윤호 (Leeyoonho02)** - [GitHub](https://github.com/Leeyoonho02)
- **김채은 (Chaeeun1117)** - [GitHub](https://github.com/Chaeeun1117)
- **김제희 (Jehee-Kim)** - [GitHub](https://github.com/Jehee-Kim)

---

## 📝 참고 문헌

### 주요 논문
1. **3D Gaussian Splatting for Real-Time Radiance Field Rendering**  
   Kerbl et al., ACM Transactions on Graphics, 2023  
   [Paper](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/) | [GitHub](https://github.com/graphdeco-inria/gaussian-splatting)

2. **VGGT: Visual Geometry Grounded Transformer**  
   Meta Research, CVPR 2025 (Best Paper Award)  
   [Project Page](https://vgg-t.github.io/) | [GitHub](https://github.com/facebookresearch/vggt)

3. **COLMAP: Structure-from-Motion and Multi-View Stereo**  
   Schönberger & Frahm, 2016  
   [Documentation](https://colmap.github.io/)

### 관련 자료
- [`Performance_Analysis/3DGS_Paper.md`](Performance_Analysis/3DGS_Paper.md) - 3DGS 논문 요약
- [`Performance_Analysis/vggt.md`](Performance_Analysis/vggt.md) - VGGT 기술 문서

---

## 📄 라이선스

본 프로젝트는 교육 목적의 캡스톤 프로젝트입니다. 

---

## 🔗 관련 링크

- [3D Gaussian Splatting Official](https://github.com/graphdeco-inria/gaussian-splatting)
- [VGGT Official](https://vgg-t.github.io/)
- [COLMAP Documentation](https://colmap.github.io/)
- [경북대학교](https://www.knu.ac.kr/)

---

## 📧 문의

프로젝트 관련 문의사항은 Issue를 통해 남겨주세요.

---

**Last Updated:** 2025-11-17
