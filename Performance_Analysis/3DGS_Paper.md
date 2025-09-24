### 영상·이미지 압축 방식이 3D Gaussian Splatting 재구성 품질에 미치는 영향

요약 (Abstract)

최근 등장한 3D Gaussian Splatting 기술은 무손실 압축 데이터셋에서 뛰어난 3D 재구성 성능과 렌더링 품질을 보여주었다. 그러나 실제 환경에서 획득되는 이미지와 동영상은 대부분 손실 압축된 형태로 제공되므로, 손실 압축 데이터에서도 안정적인 성능 확보가 필요하다. 본 논문에서는 HEVC(Random access mode)와 JPEG 압축 방식을 적용하여, 다양한 압축률에서 3D Gaussain Splatting 모델의 성능 변화를 정량적으로 분석하였다. 실험 결과, ~

Introduction

최근 컴퓨터비전 분야에서는 3D 장면을 정확하고 효율적으로 재구성하고 실시간으로 렌더링하는 기술의 연구가 활발히 진행되고 있다.

3D Gaussian Splatting은 카메라 캘리브레이션으로 얻은 sparse point cloud를 시작점으로 장면을 gaussian splat으로 표현하며,  anisotropic covariance 최적화 및 visibility-aware 렌더링을 통해 고품질의 실시간 뷰 합성을 가능하게 하는 모델이다.

기존의 NeRF 기반 기술은 픽셀마다 ray matching으로 3D point를 샘플링하기 때문에 학습과 랜더링에 많은 시간이 소요되는 반면, 3DGS는 이미지를 여러개의 Patch로 나누어 병렬 연산함으로써 속도와 효율성을 크게 향상시켰다.

그러나 대부분의 3DGS 연구는 무손실 압축 데이터셋을 기반으로 수행되었다. 
반면, 실제 환경에서 사용되는 이미지와 영상은 대부분 손실 압축 방식을 통해 제공되며. 이러한 데이터에 대해 3DGS의 재구성 품질과 렌더링 성능 변화는 충분히 연구되지 않았다.

따라서, 본 연구에서는 널리 사용되는 JPEG와 HEVC 압축 방식을 활용하여, 압축률 변화가 3DGS의 재구성 품질과 렌더링 속도에 미치는 영향을 정량적으로 분석해보고자 한다.

Related work

1. 3D Gaussain Splatting
2. Mip-NeRF360
3. JPEG, HEVC

Method

Experiment Result

Conclusion
