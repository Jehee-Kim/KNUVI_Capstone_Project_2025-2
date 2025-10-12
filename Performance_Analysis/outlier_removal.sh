QP32 Bicycle 렌더링 이상 현상 원인 요약

영상 품질 자체 문제 아님: QP32로 압축한 이미지는 눈으로 보거나 PSNR/SSIM 평가에서는 정상.
원인: SfM 단계 불안정

COLMAP에서 feature detection은 미세한 압축 노이즈에도 민감
QP32에서는 일부 영역에서 feature가 많지만 불안정하게 생성됨
그 결과 단독 관측 포인트(track length = 1)가 많아 triangulation이 제대로 되지 않음

reprojection error가 급격히 증가 → 3DGS 렌더링에서 artifact 발생

QP27, QP37 대비 비정상 현상

QP27: 압축 거의 없음 → feature 안정적 → 렌더링 정상
QP37: 압축 심해 feature 수는 적지만 안정적 → triangulation 안정 → 렌더링 회복

결론: QP32에서만 문제가 나타나는 것은 중간 압축 단계에서 SfM feature 분포가 불안정하기 때문이며, 이미지 자체 품질과는 무관.


| QP | num_points | num_images | registered images | total observations | mean track length | mean reprojection error |
| -- | ---------- | ---------- | ----------------- | ------------------ | ----------------- | ----------------------- |
| 27 | 11428      | 194        | 4585              | 41168              | 96.64             | 0.703 px                |
| 32 | 5024       | 106        | 3480              | 14490              | 98.88             | 1.037 px                |
| 37 | 3970       | 95         | 3121              | 13375              | 110.60            | 0.853 px                |

QP27: 포인트 많고 track 길이 충분 → reprojection error 낮음 → SfM 안정적
QP32: 포인트는 QP37보다 많지만 mean reprojection error 최고 → 일부 포인트 단독 관측 많음 → SfM 불안정 → 렌더링 깨짐
QP37: 포인트 수 적지만 track length 길고 reprojection error 낮음 → triangulation 안정 → 렌더링 회복


#stats.txt colmap 상세 결과 보여줌
colmap model_analyzer \
    --path "/mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets/1_bicycle/sparse/0" \
    --output_path "/mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets/1_bicycle/sparse/stats.txt"

#bin file to txt
colmap model_converter \
    --input_path "/mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets/1_bicycle/sparse/0" \
    --output_path "/mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets/1_bicycle/sparse/0_txt" \
    --output_type TXT

python3 analyze_colmap.py /mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets/1_bicycle/sparse/0_txt > qp32_analysis.txt
cat /mnt/c/Users/PC012/Desktop/BCE/HEVC_32/qp32_analysis.txt
