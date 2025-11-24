
영상·이미지 압축 방식이 3D Gaussian Splatting 렌더링 품질에 미치는 영향 분석


*배채은, *이윤호, *최희정, *문채원, **정진우, ***박상효
*경북대학교, **한국전자기술연구원, ***경북대학교(교신저자)


Effects of Image and Video Compression Methods on 3D Gaussian Splatting Rendering Quality
*Chaeeun Bae, *Yoonho Lee, *Heejung Choi, *Chaewon Moon, **Jinwoo Jeong, 
and *Sang-hyo Park
*Kyungpook National University, **Korea Electronics Technology Institute

요   약

최근 등장한 3D Gaussian Splatting 기술은 무손실 압축 데이터셋에서 뛰어난 3D 재구성 성능과 렌더링 품질을 제공하며, 가상현실, 증강현실, 3D 지도 제작 등 다양한 실제 환경의 3D 콘텐츠 제작 및 시각화에 활용되고 있다. 그러나 실제 환경에서는 저장 공간 및 네트워크 대역폭의 제약으로 인해 대부분의 영상 및 이미지 데이터가 손실 압축된 형태로 제공되므로, 압축 조건에 따른 성능 저하와 모델 민감도에 대한 분석이 필요하다. 본 논문에서는 JPEG 및 HEVC 압축 방식을 적용하여, 다양한 압축률에서 3D Gaussain Splatting 모델의 렌더링 품질 변화를 정량적으로 분석하였다. 실험 결과, JPEG는 압축률이 증가함에 따라 렌더링 품질이 급격하게 저하되는 반면, HEVC는 비교적 완만하고 예측 가능한 품질 저하 양상을 보였다. 또한 입력 데이터의 PSNR이 유사한 조건에서도 JPEG 기반 입력이 HEVC보다 일관되게 우수한 렌더링 품질을 제공함을 확인하였다.

1. 서론

최근 컴퓨터비전 분야에서는 3D 장면을 정확하고 효율적으로 재구성하고, 이를 실시간으로 렌더링하는 기술에 대한 연구가 활발히 진행되고 있다. 특히 가상현실(VR), 증강현실(AR), 디지털 트윈(Digital Twin) 등의 분야에서 고품질 3D 재구성 기술에 대한 수요가 급증하고 있다. 이러한 배경 속에서 Neural Radiance Fields (NeRF)[1]는 암시적 신경망 표현을 통해 사실적인 3D 장면 재구성을 가능하게 하며 큰 주목을 받았다. 그러나 NeRF는 픽셀 단위의 ray matching을 통해 다수의 3D point를 샘플링해야 하기 때문에 학습 및 랜더링에 많은 시간이 소요되어 실시간 응용에 제약이 있다. 이러한 한계를 극복하기 위해 제안된 3D Gaussian Splatting (3DGS)[2]은 sparse point cloud를 기반으로 장면을 Gaussian splat으로 표현하여, NeRF 대비 학습 속도와 렌더링 효율을 획기적으로 향상시켰다. 또한 3DGS는 입력 이미지를 여러개의 패치로 나누어 병렬 연산함으로써 효율성을 극대화하였으며, 이를 통해 실시간 3D 콘텐츠 생성 및 렌더링 분야에서 새로운 가능성을 제시하고 있다. 

그러나 대부분의 3DGS 관련 연구[3-5]는 무손실 압축 포맷의 이미지를 사용한 이상적인 조건에서 수행되었다. 반면 실제 환경에서는 저장 공간 및 네트워크 대역폭의 제약으로 인해 JPEG (Joint Picture Expert Group), HEVC (High Efficiency Video Coding) 등과 같은 손실 압축 방식이 광범위하게 사용된다. 특히 모바일 기기에서의 3D 콘텐츠 스트리밍, 클라우드 기반 렌더링 서비스, 대용량 3D 데이터셋의 저장 및 전송과 같은 시나리오에서는 압축이 필수적인 요소이다. 그럼에도 불구하고, 손실 압축이 3DGS의 재구성 품질 및 렌더링 성능에 미치는 영향에 대한 체계적인 연구는 충분히 이루어지지 않았다.

이미지 압축 과정에서 발생하는 정보 손실은 3DGS의 입력 데이터 품질을 저하시킬 수 있으며, 이는 3D 재구성의 기하학적 정확도와 시각적 품질에 직접적인 영향을 미칠 것으로 예상된다. 특히 3DGS는 미세한 기하학적 세부 구조와 색상 정보에 민감하므로, 압축으로 인한 정보 손실이 최종 렌더링 품질에 어떠한 영향을 미치는지 체계적으로 분석할 필요가 있다. 

그림 1 전체 실험 파이프라인[10]

따라서 본 연구에서는 압축 조건의 변화가 3DGS의 재구성 품질에 미치는 영향을 체계적으로 분석하였다. 이를 위해 이미지 압축의 대표적인 표준인 JPEG[6]과 동영상 압축 표준인 HEVC[7] 코덱을 활용하여 다양한 압축률의 데이터셋을 구성하고, 각 조건에서 3DGS 렌더링을 수행하였다. 성능 평가는 렌더링 결과를 통한 정성적 분석과 함께, PSNR, SSIM, LPIPS 세 가지 객관적 지표를 활용하여 코덱 간 성능 차이 및 동일 코덱 내 압축률 변화에 따른 품질 변화를 정량적으로 측정하였다.

2. 본론

본 연구의 전체 실험 절차는 그림 1과 같다. Mip-NeRF 360 데이터셋[8]의 8배 다운스케일링 버전을 입력으로 하여, JPEG과 HEVC 두 가지 코덱을 적용하였다. 그림에서 상단 가지는 HEVC 기반 압축 과정, 하단 가지는 JPEG 압축 과정을 나타낸다. HEVC의 경우, 원본 이미지 시퀀스를 영상 압축 코덱의 입력 형식에 맞추기 위해 전처리를 과정을 거쳤다. 촬영 간격이 고르지 않은 3개의 장면(bicycle, flowers, treehill)은 원본 데이터에서 홀수·짝수 프레임이 서로 다른 카메라 경로를 이루어 그대로 사용할 경우 시점 전환이 불연속적으로 나타났다. 이에 따라 홀수 프레임은 내림차순, 짝수 프레임은 오름차순으로 정렬함으로써 시점 변화를 완화하였다. 정렬된 이미지 시퀀스를 ffmpeg을 사용하여 YUV 4:4:4 8-bit raw video로 변환하고, framerate는 30fps로 설정하였다. 실험 편의를 위해 해상도가 홀수인 장면은 짝수 단위로 조정하였다. 이후 Random Access 모드 기반으로 인코딩 및 디코딩하여 압축된 프레임 시퀀스를 생성하였다. JPEG의 경우, 별도의 전처리 과정 없이 바로 이미지 단위 압축을 적용하였다.

각 압축된 데이터셋은 Structure-from-Motion (SfM)[9]을 통해 카메라 포즈와 희소한 포인트 클라우드를 복원하였으며, 이를 3DGS의 입력으로 사용하였다. 최종적으로 3DGS를 통해 각 압축 조건에서의 재구성 및 렌더링 결과를 획득하였다.

표 .압축 수준별 JPEG 압축 결과와 해당 데이터를 이용한 3DGS 렌더링 품질 비교


표 2 압축 수준별 HEVC 압축 결과와 해당 데이터를 이용한 3DGS 렌더링 품질 비교


3. 실험

3.1. 실험 환경 및 평가 방법
모든 실험은 NVIDIA GeForce RTX 3080 GPU 환경에서 진행하였으며, 3DGS 모델은 PyTorch 기반의 공식 구현을 활용하였다.
평가 지표로는 PSNR, SSIM, LPIPS를 사용하여 (1) 원본 이미지와 압축된 이미지 간, (2) 원본 이미지와 압축 후 렌더링 결과 간의 차이를 정량적으로 측정하였다. 

3.2. 실험 설정
이 절에서는 그림 1의 절차에 따라 수행한 실험의 구체적인 설정값과 평가 방법을 기술한다.

3.2.1 JPEG 코덱 
Quality Factor (QF)를 10, 30, 50, 70, 90으로 설정하였다.

3.2.2 HEVC 코덱
전처리 과정을 거친 데이터셋을 HEVC reference software인 HM 16.22으로 인코딩하였다. Random Access 모드에서 압축 수준을 달리하기 위해 QP값을 27, 32, 37, 42로 설정하였다. 인코딩 설정은 Profile main-RExt, inputChromaFormat 444를 사용하였으며, ConformanceWindowMode=1을 통해 자동 패딩을 적용하였다. 인코딩 후 재구성된 YUV 파일은 ffmpeg을 통해 PNG 형식으로 변환하여 평가에 사용하였다.  이후 압축된 데이터셋을 기반으로 SfM 및 3DGS 렌더링을 수행하고, 성능을 정량적으로 평가하였다. 

3. 실험 결과
3.1. JPEG 압축에 따른 렌더링 품질 변화
JPEG QF 10, 30, 50, 70, 90 조건에서 각각 3DGS 렌더링을 수행하고, 9개 장면에 대한 평균 수치를 계산하였다. 먼저 비압축 조건과 압축 조건의 렌더링 결과를 비교하여, 압축률에 따른 성능 저
그림 2 garden 장면의 JPEG 압축률에 따른 3DGS 렌더링품질 변화
하 양상을 분석하였다. 표 1에서 확인할 수 있듯이, 압축률이 높아질수록 렌더링 품질 저하 폭이 비선형적으로 증가하는 경향이 관찰되었다. 특히 QF 30 이하의 고압축 구간에서는 PSNR 및 SSIM 감소율과 LPIPS 증가율이 급격히 커졌다. 이는 고압축 과정에서 고주파 성분이 크게 손실되어 시각적 품질 저하가 가속화되기 때문으로 해석된다. 그림 2에서도 압축 손실이 적은 JPEG 90 및 70 구간에서는 렌더링 후 결과가 원본 이미지와 유사한 반면, 압축률이 높아질수록 세부 구조가 손실되어 디테일이 뭉개지는 현상을 시각적으로 확인할 수 있다.
그림 3 JPEG 압축 데이터에 비해 렌더링 후 데이터의 SSIM 수치가 상승한 bonsai 장면

그림  압축 방식에 따른 PSNR 비교

다음으로 압축 결과와 압축된 데이터를 이용해 렌더링한 결과를 비교하여, 압축률이 렌더링 품질에 미치는 영향을 분석하였다. 표 1에서 볼 수 있듯이, JPEG 품질 계수가 높을수록(즉, 압축률이 낮을수록) 렌더링 전후의 품질 차이가 더 크게 나타나는 경향을 보인다. 이는 고압축 구간에서는 세부 정보가 이미 소실되어 품질 차이가 상대적으로 작기 때문으로 해석된다.
또한 일부 장면에서는 압축 결과보다 압축된 데이터를 기반으로 렌더링한 결과의 SSIM 값이 오히려 더 높게 측정되는 현상이 관찰되었다. 특히 QF 10 또는 30과 같은 고압축 구간에서 이 경향이 두드러졌는데, 이는 3DGS 렌더링 과정에서 JPEG의 blocking artifact가 일부 완화(smoothing)되는 효과가 반영된 결과로 보인다.[11] 그림 3의 JPEG QF 10 예시에서도, 압축 후 이미지에서는 artifact가 뚜렷하지만 렌더링 후 이미지에서는 완화된 모습을 시각적으로 확인할 수 있다.
3.2. HEVC 압축에 따른 렌더링 품질 변화
HEVC QP 27, 32, 37, 42에 대해 각각 3DGS 렌더링을 수행하고, 9개 장면의 평균 수치를 계산하였다. JPEG과 동일하게 비압축 렌더링 결과와 압축 렌더링 결과를 비교하여 압축률에 따른 성능 저하를 분석하였다. 표 2의 결과를 보면 HEVC는 압축률이 높아질수록 품질 저하가 점진적으로 증가하는 경향을 보여, JPEG 대비 상대적으로 완만한 감소 패턴을 나타냈다. 다음으로 압축 결과와 압축 데이터의 렌더링 결과를 비교했을 때,  JPEG과 달리 압축률의 차이가 렌더링 품질에 뚜렷한 영향을 미치지 않는 것으로 나타났다.
대부분의 실험 결과에서 압축률이 증가할수록 렌더링 품질이 점진적으로 저하되는 경향을 보였다. 그러나 하나의 예외적인 경우가 관찰되었다. HEVC QP 32 조건의 bicycle 장면에서는 입력 데이터에 이상이 없음에도 불구하고, 렌더링 결과의 PSNR이 14.56으로 측정되어 QP 42 조건의 16.742보다 오히려 낮은 값을 보였다. 이에 SfM 단계를 분석한 결과, QP 32에서 평균 재투영 오차가 1.037 px로 급격히 증가한 것으로 확인되었다(QP 27: 0.703 px, QP 37: 0.853 px). 이는 중간 압축 단계에서 SfM 특징점의 분포가 불안정해지며, 3DGS 렌더링 과정에서 오류가 증폭된 것으로 해석된다.
3.3 압축 코덱에 따른 렌더링 품질 변화
JPEG과 HEVC 간의 성능을 비교해봤을 때, 압축 후 3DGS 입력 데이터셋의 PSNR 수치가 유사한 조건에서 항상 JPEG의 렌더링 결과가 우수한 것을 확인할 수 있었다. 그림4에서 JPEG QF 10, 30, 50은 각각 HEVC QP 37, 32, 27에 대응된다. 압축 후의 데이터에서는 HEVC의 PSNR 수치가 더 높지만, 렌더링 이후에는 JPEG이 더 높은 품질을 보이는 현상을 확인할 수 있다. 이는 두 코덱의 압축 방식 차이에서 기인한다. JPEG은 각 프레임을 독립적으로 압축하는 Intra-frame 방식을 사용한다. 이 경우 프레임 간의 정보가 서로 영향을 주지 않아, 입력 영상의 시간적 일관성이 잘 유지된다. 반면 HEVC Random Access 모드는 Inter-frame 방식을 사용해, 이전 또는 이후 프레임을 참고하여 현재 프레임을 압축한다. 이렇게 하면 압축 효율은 높아지지만, 프레임 간 예측 과정에서 발생한 오차가 누적되어 시점 간 불일치가 발생할 수 있다. 이러한 불일치는 3DGS의 파라미터 추정 과정에 노이즈로 작용하여, 결과적으로 렌더링 품질이 저하된 것으로 해석된다.

4. 결론
   
본 연구에서는 3DGS 기반의 3D 재구성 과정에서 압축 코덱 및 압축률이 렌더링 품질에 미치는 영향을 정량적으로 분석하였다. JPEG 및 HEVC 두 가지 대표적인 손실 압축 코덱을 적용하여 다양한 압축 조건에서 3DGS 성능을 비교하였다. 실험 결과, JPEG은 압축률 증가 시 PSNR·SSIM 감소와 LPIPS 증가가 비선형적으로 나타난 반면, HEVC는 비교적 점진적인 품질 저하를 보였다. 또한 입력 데이터셋이 유사한 PSNR 조건에서도 JPEG 기반 입력이 HEVC보다 렌더링 품질이 안정적이었으며, 이는 JPEG의 프레임 독립적 압축 방식 덕분으로 판단된다. 이러한 결과는 3DGS 기반의 3D 콘텐츠 제작이나 스트리밍 환경에서 코덱 선택과 압축률이 최종 렌더링 품질에 실질적인 영향을 미칠 수 있음을 시사한다. 특히 실시간 렌더링 또는 대규모 데이터셋 처리와 같은 응용 환경에서는 단순히 압축 효율이 아닌 시점 간 일관성과 시각적 품질 간의 균형을 고려한 코덱 선택 및 전처리 전략이 필요하다. 향후 연구에서는 본 연구에서 다루지 못한 최신 비디오 코덱(VVC, AV1 등)과 학습 기반 비디오 압축 방식을 포함하여 3DGS와의 상호작용을 비교하는 보다 포괄적인 분석이 필요할 것으로 보인다.

REFERENCES
[1] B. Mildenhall, P. P. Srinivasan, M. Tancik, J. T. Barron, R. Ramamoorthi, and R. Ng, “NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), pp. 500–509, Jun. 2020.

[2] B. Kerbl, G. Kopanas, T. Leimkühler, and G. Drettakis, "3D Gaussian Splatting for Real-Time Radiance Field Rendering" ACM Trans. Graph., vol. 42, no. 4, pp. 1–12, Jul. 2023.

[3] G. Wu, T. Yi, J. Fang, L. Xie, X. Zhang, W. Wei, W. Liu, Q. Tian, and X. Wang, “4D Gaussian Splatting for Real-Time Dynamic Scene Rendering,” in Proc. CVPR, pp. 20310–20320, 2024.

[4] J. C. Lee, D. Rho, X. Sun, J. H. Ko, and E. Park, “Compact 3D Gaussian Representation for Radiance Field,” in Proc. CVPR, pp. 21719–21728, Seattle, United States, Jun. 2024.

[5] Y. Liu, H. Guan, C. Luo, L. Fan, N. Wang, J. Peng, and Z. Zhang, “CityGaussian: Real-time High-quality Large-Scale Scene Rendering with Gaussians,” in Proc. ECCV, pp. 265–282, Oct. 2024.

[6] G. K. Wallace, “The JPEG still picture compression standard,” Commun. ACM, vol. 34, no. 4, pp. 30–44, Apr. 1991.

[7] G. J. Sullivan, J. Ohm, W. J. Han, and T. Wiegand, “Overview of the High Efficiency Video Coding (HEVC) Standard,” IEEE Trans. Circuits Syst. Video Technol., vol. 22, no. 12, pp. 1649–1668, Dec. 2012.

[8] J. T. Barron, B. Mildenhall, D. Verbin, P. P. Srinivasan, and P. Hedman, “Mip-NeRF 360: Unbounded Anti-Aliased Neural Radiance Fields,” in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR), pp. 5470–5479, Jun. 2022.

[9] J. L. Schönberger and J.-M. Frahm, “Structure-from-Motion Revisited,” in Proc. CVPR, pp. 4104–4113, Jun. 2016.

[10] Image credit: Tetromino, Wikimedia Commons, CC BY 3.0

[11] R. Pourreza-Shahri, S. Yousefi and N. Kehtarnavaz, "Optimization method to reduce blocking artifacts in JPEG images" Journal of Electronic Imaging, vol. 23, no. 6, pp. 1–12, Nov/Dec 2014.
