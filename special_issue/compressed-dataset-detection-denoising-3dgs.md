## 영상·이미지 압축 환경에서 3D Gaussian Splatting 렌더링 품질 향상을 위한 압축 데이터셋 및 탐지-디노이징 프레임워크

### A Compressed Dataset and a Detection-Denoising Framework for Enhancing 3D Gaussian Splatting Rendering under Video and Image Compression

---

### 요 약 (Abstract)

최근 등장한 **3D Gaussian Splatting (3DGS)** 기술은 무손실 압축 데이터셋에서 뛰어난 3D 재구성 성능과 렌더링 품질을 제공하며, 가상현실, 증강현실, 3D 지도 제작 등 다양한 실제 환경의 3D 콘텐츠 제작 및 시각화에 활용되고 있다. 
그러나 실제 환경에서는 저장 공간 및 네트워크 대역폭의 제약으로 인해 대부분의 영상 및 이미지 데이터가 **손실 압축된 형태**로 제공되므로, 압축 조건에 따른 성능 저하와 모델 민감도에 대한 분석이 필요하다.
본 논문에서는 **JPEG** 및 **HEVC** 압축 방식을 적용하여, 다양한 압축률에서 3D Gaussian Splatting 모델의 렌더링 품질 변화를 정량적 및 정성적으로 분석하였다. 실험 결과, **JPEG는 압축률이 증가함에 따라 렌더링 품질이 급격하게 저하**되는 반면, 
**HEVC는 비교적 완만한 품질 저하 양상**을 보였다. 또한 입력 데이터의 PSNR이 유사한 조건에서도 **JPEG 기반 입력이 HEVC보다 일관되게 우수한 렌더링 품질**을 제공함을 확인하였다.

Abstract
Recently, 3D Gaussian Splatting has demonstrated outstanding 3D reconstruction performance and high rendering quality when trained on lossless datasets, 
and it has been widely adopted in practical applications such as virtual reality (VR), augmented reality (AR), and 3D mapping. 
However, in real-world environments, most image and video data are provided in lossy compressed form due to storage and network bandwidth limitations, 
making it necessary to analyze performance degradation and model sensitivity under compression conditions.
In this paper, we apply JPEG and HEVC compression to input sequences and quantitatively and qualitatively investigate the change in rendering quality of the 3D Gaussian Splatting model across various compression levels. 
Experimental results show that JPEG experiences a steep decline in rendering quality as the compression ratio increases, whereas HEVC exhibits a comparatively gradual degradation trend. 
In addition, even under similar PSNR conditions, JPEG-compressed inputs consistently yield higher rendering quality than HEVC-compressed inputs.

* **Keyword**: 3D Gaussian Splatting, Compressed Dataset, Artifact Detection, Denoising, Rendering Quality

---

## Ⅰ. 서 론 (Introduction)

최근 컴퓨터비전 분야에서는 3D 장면을 정확하고 효율적으로 재구성하고, 이를 실시간으로 렌더링하는 기술에 대한 연구가 활발히 진행되고 있다. 
특히 가상현실(VR), 증강현실(AR), 디지털 트윈(Digital Twin) 등의 분야에서 고품질 3D 재구성 기술에 대한 수요가 급증하고 있다. 
이러한 배경 속에서 **Neural Radiance Fields (NeRF)**\[1]는 암시적 신경망 표현을 통해 사실적인 3D 장면 재구성을 가능하게 하며 큰 주목을 받았다. 
그러나 NeRF는 픽셀 단위의 ray matching을 통해 다수의 3D point를 샘플링해야 하기 때문에 학습 및 렌더링에 많은 시간이 소요되어 실시간 응용에 제약이 있다.

이러한 한계를 극복하기 위해 제안된 **3D Gaussian Splatting (3DGS)**\[2]은 sparse point cloud를 기반으로 장면을 Gaussian splat으로 표현하여, 
NeRF 대비 학습 속도와 렌더링 효율을 획기적으로 향상시켰다. 또한 3DGS는 입력 이미지를 여러 개의 패치로 나누어 병렬 연산함으로써 효율성을 극대화하였으며, 
이를 통해 실시간 3D 콘텐츠 생성 및 렌더링 분야에서 새로운 가능성을 제시하고 있다.

그러나 대부분의 3DGS 관련 연구\[3-5]는 **무손실 압축 포맷**의 이미지를 사용한 이상적인 조건에서 수행되었다. 
반면 실제 환경에서는 저장 공간 및 네트워크 대역폭의 제약으로 인해 **JPEG** (Joint Picture Expert Group), **HEVC** (High Efficiency Video Coding) 등과 같은 **손실 압축 방식**이 광범위하게 사용된다. 
특히 모바일 기기에서의 3D 콘텐츠 스트리밍, 클라우드 기반 렌더링 서비스, 대용량 3D 데이터셋의 저장 및 전송과 같은 시나리오에서는 압축이 필수적인 요소이다. 
그럼에도 불구하고, 손실 압축이 3DGS의 재구성 품질 및 렌더링 성능에 미치는 영향에 대한 체계적인 연구는 충분히 이루어지지 않았다.

이미지 압축 과정에서 발생하는 정보 손실은 3DGS의 입력 데이터 품질을 저하시킬 수 있으며, 이는 3D 재구성의 기하학적 정확도와 시각적 품질에 직접적인 영향을 미칠 것으로 예상된다. 
특히 3DGS는 미세한 기하학적 세부 구조와 색상 정보에 민감하므로, 압축으로 인한 정보 손실이 최종 렌더링 품질에 어떠한 영향을 미치는지 체계적으로 분석할 필요가 있다.

따라서 본 연구에서는 압축 조건의 변화가 3DGS의 재구성 품질에 미치는 영향을 체계적으로 분석하였다. 
이를 위해 이미지 압축의 대표적인 표준인 **JPEG**\[6]과 동영상 압축 표준인 **HEVC**\[7] 코덱을 활용하여 다양한 압축률의 데이터셋을 구성하고, 각 조건에서 3DGS 렌더링을 수행하였다. 
성능 평가는 렌더링 결과를 통한 정성적 분석과 함께, **PSNR, SSIM, LPIPS** 세 가지 객관적 지표를 활용하여 코덱 간 성능 차이 및 동일 코덱 내 압축률 변화에 따른 품질 변화를 정량적으로 측정하였다.

| **QF** | **JPEG** **PSNR↑** | **JPEG** **SSIM↑** | **JPEG** **LPIPS↓** | **Rendered** **PSNR** | **Rendered** **SSIM** | **Rendered** **LPIPS** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| raw | - | - | - | 27.397 | 0.859 | 0.085 |
| 90 | 35.835 | 0.960 | 0.012 | 27.027 | 0.846 | 0.097 |
| 70 | 31.287 | 0.906 | 0.046 | 26.454 | 0.821 | 0.134 |
| 50 | 29.679 | 0.871 | 0.084 | 25.624 | 0.787 | 0.173 |
| 30 | 28.070 | 0.825 | 0.149 | 25.366 | 0.767 | 0.218 |
| 10 | 24.462 | 0.673 | 0.345 | 22.611 | 0.617 | 0.367 |

| **QP** | **HEVC** **PSNR↑** | **HEVC** **SSIM↑** | **HEVC** **LPIPS↓** | **Rendered** **PSNR↑** | **Rendered** **SSIM↑** | **Rendered** **LPIPS↓** |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Raw | - | - | - | 27.397 | 0.859 | 0.085 |
| 27 | 30.781 | 0.871 | 0.099 | 25.527 | 0.752 | 0.195 |
| 32 | 28.335 | 0.777 | 0.211 | 23.782 | 0.652 | 0.326 |
| 37 | 25.731 | 0.672 | 0.345 | 21.542 | 0.543 | 0.435 |
| 42 | 24.022 | 0.580 | 0.455 | 20.420 | 0.481 | 0.557 |

| Scene | bicycle | bonsai | counter | flowers | garden | kitchen | room | stump | treehill |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| Rendered Raw | 23.109 | 31.725 | 28.767 | 22.034 | 29.100 | 31.419 | 31.048 | 27.091 | 22.281 |
| JPEG 90 | 36.286 | 37.320 | 36.115 | 33.974 | 34.422 | 34.984 | 37.914 | 35.389 | 36.107 |
| JPEG 70 | 30.995 | 32.904 | 32.041 | 28.737 | 30.197 | 30.440 | 34.092 | 31.129 | 31.052 |
| JPEG 50 | 29.059 | 31.202 | 30.491 | 26.977 | 28.671 | 28.831 | 32.526 | 30.141 | 29.210 |
| JPEG 30 | 27.285 | 29.634 | 28.994 | 25.467 | 27.298 | 27.433 | 30.931 | 27.961 | 27.624 |
| JPEG 10 | 24.381 | 22.218 | 25.588 | 22.617 | 24.466 | 24.570 | 27.456 | 24.923 | 23.940 |
| Rendered JPEG 90 | 22.860 | 30.968 | 28.548 | 21.915 | 28.806 | 30.982 | 30.609 | 26.493 | 22.063 |
| Rendered JPEG 70 | 22.670 | 29.901 | 28.053 | 21.701 | 27.776 | 29.691 | 30.390 | 25.992 | 21.912 |
| Rendered JPEG 50 | 22.445 | 29.730 | 27.781 | 21.579 | 27.269 | 28.819 | 29.771 | 21.345 | 21.874 |
| Rendered JPEG 30 | 21.657 | 28.677 | 27.115 | 21.109 | 26.127 | 27.800 | 29.341 | 24.870 | 21.596 |
| Rendered JPEG 10 | 20.905 | 21.294 | 25.313 | 18.820 | 24.684 | 24.985 | 27.172 | 22.140 | 18.182 |
| HEVC 27 | 28.342 | 34.051 | 33.126 | 26.714 | 30.470 | 32.337 | 34.899 | 29.631 | 27.458 |
| HEVC 32 | 24.779 | 31.563 | 30.890 | 24.256 | 27.945 | 30.045 | 32.78 | 26.223 | 26.533 |
| HEVC 37 | 23.214 | 28.661 | 28.124 | 22.951 | 25.546 | 24.345 | 29.489 | - | 23.516 |
| HEVC 42 | 20.821 | 25.480 | 25.606 | - | 23.572 | 22.623 | 26.032 | - | - |
| Rendered HEVC 27 | 22.386 | 29.707 | 28.021 | 20.882 | 26.812 | 29.221 | 29.902 | 21.992 | 20.824 |
| Rendered HEVC 32 | 14.562 | 28.429 | 27.130 | 20.305 | 25.363 | 27.463 | 28.18 | 22.126 | 20.478 |
| Rendered HEVC 37 | 18.894 | 26.202 | 25.644 | 15.881 | 23.376 | 23.950 | 26.482 | x | 11.909 |
| Rendered HEVC 42 | 16.742 | 24.024 | 23.768 | x | 21.885 | 22.709 | 13.389 | x | x |

---

## Ⅱ. 본론 (Main)

본 연구의 전체 실험 절차는 [그림 1]과 같다. 
Mip-NeRF 360 데이터셋\[8]의 8배 다운스케일링 버전을 입력으로 하여, **JPEG**과 **HEVC** 두 가지 코덱을 적용하였다. 
그림에서 상단 가지는 HEVC 기반 압축 과정, 하단 가지는 JPEG 압축 과정을 나타낸다.

### 2.1. HEVC 압축을 위한 전처리 및 인코딩

HEVC의 경우, 원본 이미지 시퀀스를 영상 압축 코덱의 입력 형식에 맞추기 위해 전처리를 과정을 거쳤다.

* 촬영 간격이 고르지 않은 3개의 장면(`bicycle`, `flowers`, `treehill`)은 원본 데이터에서 홀수·짝수 프레임이 서로 다른 카메라 경로를 이루어 그대로 사용할 경우 시점 전환이 불연속적으로 나타났다.
    * 이에 따라 홀수 프레임은 내림차순, 짝수 프레임은 오름차순으로 정렬함으로써 시점 변화를 완화하였다.
* 정렬된 이미지 시퀀스를 `ffmpeg`을 사용하여 **YUV 4:4:4 8-bit raw video**로 변환하고, framerate는 **30fps**로 설정하였다.
* 실험 편의를 위해 해상도가 홀수인 장면은 짝수 단위로 조정하였다.
* 이후 **Random Access 모드** 기반으로 인코딩 및 디코딩하여 압축된 프레임 시퀀스를 생성하였다.

### 2.2. JPEG 압축

* JPEG의 경우, 별도의 전처리 과정 없이 바로 이미지 단위 압축을 적용하였다.

### 2.3. 3DGS 렌더링 입력 준비

* 각 압축된 데이터셋은 **Structure-from-Motion (SfM)**\[9]을 통해 카메라 포즈와 희소한 포인트 클라우드를 복원하였으며, 이를 3DGS의 입력으로 사용하였다.
* 최종적으로 3DGS를 통해 각 압축 조건에서의 재구성 및 렌더링 결과를 획득하였다.

---

## Ⅲ. 실험 (Experiments)

### 3.1. 실험 환경 및 평가 방법

* 모든 실험은 **NVIDIA GeForce RTX 3080 GPU** 환경에서 진행하였으며, 3DGS 모델은 PyTorch 기반의 공식 구현을 활용하였다.
* 평가 지표로는 **PSNR, SSIM, LPIPS**를 사용하여 다음 두 가지 차이를 정량적으로 측정하였다.
    1.  원본 이미지와 압축된 이미지 간 (입력 품질)
    2.  원본 이미지와 압축 후 렌더링 결과 간 (출력 품질)

### 3.2. 실험 설정

#### 3.2.1. JPEG 코덱

* **Quality Factor (QF)**를 **10, 30, 50, 70, 90**으로 설정하였다.

#### 3.2.2. HEVC 코덱

* 전처리 과정을 거친 데이터셋을 HEVC reference software인 **HM 16.22**으로 인코딩하였다.
* Random Access 모드에서 압축 수준을 달리하기 위해 **QP값**을 **27, 32, 37, 42**로 설정하였다.
* 인코딩 설정은 **Profile main-RExt, inputChromaFormat 444**를 사용하였으며, ConformanceWindowMode=1을 통해 자동 패딩을 적용하였다.
* 인코딩 후 재구성된 YUV 파일은 `ffmpeg`을 통해 PNG 형식으로 변환하여 평가에 사용하였다.
* 이후 압축된 데이터셋을 기반으로 SfM 및 3DGS 렌더링을 수행하고, 성능을 정량적으로 평가하였다.

### 3.3. 실험 결과

#### 3.3.1. JPEG 압축에 따른 렌더링 품질 변화

* JPEG QF 10, 30, 50, 70, 90 조건에서 각각 3DGS 렌더링을 수행하고, 9개 장면에 대한 평균 수치를 계산하였다.
* **성능 저하 양상**: 압축률이 높아질수록 렌더링 품질 저하 폭이 **비선형적으로 증가**하는 경향이 관찰되었다 (표 1).
    * 특히 QF 30 이하의 고압축 구간에서는 PSNR 및 SSIM 감소율과 LPIPS 증가율이 **급격히 커졌다**.
    * 이는 고압축 과정에서 고주파 성분이 크게 손실되어 시각적 품질 저하가 가속화되기 때문으로 해석된다.
* **시각적 품질**: 압축 손실이 적은 JPEG 90 및 70 구간에서는 렌더링 후 결과가 원본 이미지와 유사한 반면, 압축률이 높아질수록 세부 구조가 손실되어 디테일이 뭉개지는 현상을 시각적으로 확인할 수 있다 (그림 2). 

#### 3.3.2. HEVC 압축에 따른 렌더링 품질 변화

* HEVC QP 27, 32, 37, 42에 대해 각각 3DGS 렌더링을 수행하고, 9개 장면의 평균 수치를 계산하였다.
* **성능 저하 양상**: HEVC는 압축률이 높아질수록 품질 저하가 **점진적으로 증가**하는 경향을 보여, JPEG 대비 **상대적으로 완만한 감소 패턴**을 나타냈다 (표 2).
* **SfM 오차 및 예외**:
    * HEVC QP 32 조건의 `bicycle` 장면에서는 입력 데이터에 이상이 없음에도 불구하고, 렌더링 결과의 PSNR이 **14.56**으로 측정되어 QP 42 조건의 16.742보다 오히려 낮은 값을 보였다.
    * SfM 단계를 분석한 결과, QP 32에서 평균 재투영 오차가 **1.037 px**로 급격히 증가한 것으로 확인되었다 (QP 27: $0.703 \text{ px}$, QP 37: $0.853 \text{ px}$). 이는 중간 압축 단계에서 SfM 특징점의 분포가 불안정해지며, 3DGS 렌더링 과정에서 오류가 증폭된 것으로 해석된다.
* **실험 실패**: 표 3을 보면, 일부 장면의 QP 37 이상 고압축 조건에서는 압축으로 인한 심각한 품질 저하로 인해 **SfM 추정 자체가 실패**하여 3DGS 실험을 수행할 수 없었다.

#### 3.3.3. 압축 코덱에 따른 렌더링 품질 변화

* **JPEG의 일관된 우세**: 압축 후 3DGS 입력 데이터셋의 PSNR 값이 유사한 조건에서 렌더링 결과의 PSNR은 **JPEG이 HEVC보다 항상 높게** 나타나는 현상을 확인할 수 있다 (표 3).
* **유사 PSNR 비교**: 그림 4에서 JPEG QF 10, 30, 50은 각각 HEVC QP 37, 32, 27과 수치를 비교해볼 수 있다. 세 쌍 모두 압축 후의 데이터에서는 HEVC의 PSNR 수치가 더 높지만, **렌더링 이후에는 JPEG이 더 높은 수치**를 보인다.
* **원인 분석 (코덱 방식 차이)**:
    * **JPEG**: 모든 프레임을 독립적으로 압축하는 **Intra-frame** 방식을 사용한다. 프레임 간의 정보가 서로 영향을 주지 않아, 압축 과정에서 **시간적 일관성**이 비교적 잘 보존된다.
    * **HEVC**: Random Access 모드는 이전 또는 이후 프레임을 참고하여 현재 프레임을 압축하는 **Inter-frame** 방식을 사용한다. 이는 높은 압축 효율을 제공하지만, 프레임 간 예측 과정에서 발생한 오차가 누적되어 **시점 간 불일치**가 발생할 수 있다.
* **결론**: 3DGS는 여러 관측 시점 간의 일관성을 기반으로 파라미터를 최적화하므로, HEVC의 누적된 시점 예측 오차가 최적화 과정에 노이즈로 작용하여 최종 렌더링 품질을 저하시킨 것으로 해석된다. 
    * 단, 본 분석은 비트레이트가 아닌 렌더링 전후 PSNR 수치를 기반으로 한 비교임을 명시한다.

---

## Ⅳ. 결론 (Conclusion)

본 연구에서는 3DGS 기반의 3D 재구성 과정에서 압축 코덱 및 압축률이 렌더링 품질에 미치는 영향을 정량적으로 분석하였다. 
JPEG 및 HEVC 두 가지 대표적인 손실 압축 코덱을 적용하여 다양한 압축 조건에서 3DGS 성능을 비교하였다. 
실험 결과, JPEG은 압축률 증가 시 PSNR·SSIM 감소와 LPIPS 증가가 비선형적으로 나타난 반면, HEVC는 비교적 점진적인 품질 저하를 보였다. 
또한 입력 데이터셋이 유사한 PSNR 조건에서도 JPEG 기반 입력이 HEVC보다 렌더링 품질이 안정적이었으며, 
이는 JPEG의 프레임 독립적 압축 방식 덕분으로 판단된다. 이러한 결과는 3DGS 기반의 3D 콘텐츠 제작이나 스트리밍 환경에서 코덱 선택과 압축률이 최종 렌더링 품질에 실질적인 영향을 미칠 수 있음을 시사한다.
특히 실시간 렌더링 또는 대규모 데이터셋 처리와 같은 응용 환경에서는 단순히 압축 효율이 아닌 시점 간 일관성과 시각적 품질 간의 균형을 고려한 코덱 선택 및 전처리 전략이 필요하다. 
향후 연구에서는 본 연구의 결과를 바탕으로, 압축된 입력 데이터의 3DGS 렌더링 품질을 사전에 판별하기 위한 탐지 네트워크를 구축할 예정이다. 
구체적으로, 다양한 압축률을 적용한 데이터셋을 입력으로 하는 3DGS 렌더링 결과에 대해 PSNR 기반의 품질 판별 임계값을 설정하고, 
이를 기준으로 입력 이미지를 1/0으로 라벨링하여 학습 데이터로 사용할 계획이다. PSNR이 임계값 이상인 경우는 고품질(1), 미만인 경우는 저품질(0)로 정의하며, 
임계값은 원본과의 PSNR 차이를 기준으로 실험적으로 도출한다. 이렇게 얻어진 라벨링 데이터를 기반으로 3DGS 렌더링 품질을 사전에 예측하는 이진 분류 모델을 학습한다. 
이후 탐지 네트워크가 저품질로 판단한 입력에 대해서는 디노이징 모델을 적용해 복원을 수행하며, 
품질이 양호한 입력은 그대로 3DGS에 사용함으로써, 압축 환경에서도 안정적인 3D 재구성 성능을 달성할 수 있는 탐지-디노이징 파이프라인을 구현하고자 한다.

---

## 참 고 문 헌 (References)

\[1] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis,” in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, pp. 500–509, Jun. 2020. DOI:10.1007/978‑3‑030‑58452‑8_24

\[2] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, "3D Gaussian Splatting for Real-Time Radiance Field Rendering" *ACM Trans. Graph*, vol. 42, no. 4, pp. 112, Jul. 2023. DOI:10.1145/3592433

\[3] G. Wu, T. Yi, J. Fang, L. Xie, X. Zhang, W. Wei, W. Liu, Q. Tian, and X. Wang, “4D Gaussian Splatting for Real-Time Dynamic Scene Rendering,” in *Proc. CVPR*, pp. 20310–20320, 2024. DOI:10.1109/CVPR52733.2024.01920

\[4] J. C. Lee, D. Rho, X. Sun, J. H. Ko, and E. Park, “Compact 3D Gaussian Representation for Radiance Field,” in *Proc. CVPR*, pp. 21719–21728, Seattle, United States, Jun. 2024. DOI:10.1109/CVPR52733.2024.02052

\[5] Y. Liu, H. Guan, C. Luo, L. Fan, N. Wang, J. Peng, and Z. Zhang, “CityGaussian: Real-time High-quality Large-Scale Scene Rendering with Gaussians,” in *Proc. ECCV*, pp. 265–282, Oct. 2024. DOI:10.1007/978-3-031-72640-8_15

\[6] G. K. Wallace, “The JPEG still picture compression standard,” *Commun. ACM,* vol. 34, no. 4, pp. 30–44, Apr. 1991.

\[7] G. J. Sullivan, J. Ohm, W. J. Han, and T. Wiegand, “Overview of the High Efficiency Video Coding (HEVC) Standard,” *IEEE Trans. Circuits Syst. Video Technol.*, vol. 22, no. 12, pp. 1649–1668, Dec. 2012. DOI:10.1109/TCSVT.2012.2221191

\[8] J. T. Barron, B. Mildenhall, D. Verbin, P. P. Srinivasan, and P. Hedman, “Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields,” in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, pp. 5470–5479, Jun. 2022. DOI: 10.1109/CVPR52688.2022.00539

\[9] J. L. Schönberger and J.-M. Frahm, “Structure-from-Motion Revisited,” in *Proc. CVPR*, pp. 4104–4113, Jun. 2016. DOI: 10.1109/CVPR.2016.445.

\[10] R. Pourreza-Shahri, S. Yousefi and N. Kehtarnavaz, "Optimization method to reduce blocking artifacts in JPEG images" *Journal of Electronic Imaging*, vol. 23, no. 6, pp. 1–12, Nov/Dec 2014. DOI: 10.1117/1.JEI.23.6.063023.
