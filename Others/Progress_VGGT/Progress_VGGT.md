### Dataset

CO3Dv2 Dataset 에서 11 scene 선별

https://github.com/facebookresearch/co3d?tab=readme-ov-file

각 frame에 Random codec, Random quality로 압축

Codec은 JPEG, JPEG2000, HEIC로 선정

Quality는 10-100사이로 선정

### 실험

VGGT input으로 각 프레임 1장씩 넣고 결과 확인

1. Compression Quality - Point Cloud 수에 대한 관계
    
    관계가 보이지 않음. -> Chamfer distance, Downstream Task에서의 성능 분석 필요

<img width="800" height="600" alt="all_codecs_Q_vs_points_colored" src="https://github.com/user-attachments/assets/c4216bf8-0149-404f-b17a-8e98dd4993f2" />
<img width="800" height="600" alt="HEIC_Q_vs_points" src="https://github.com/user-attachments/assets/a6e813e8-c610-4da0-a3fb-4c5d5f8271f1" />
<img width="800" height="600" alt="JPEG_Q_vs_points" src="https://github.com/user-attachments/assets/924f3055-3edc-4d7a-8803-58d3c22b3d22" />
<img width="800" height="600" alt="JPEG2000_Q_vs_points" src="https://github.com/user-attachments/assets/2e1d3e97-c8f1-4834-b5c8-7ff9dea31fab" />


2. Chamfer distance
