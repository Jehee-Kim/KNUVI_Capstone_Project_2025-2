import os
import subprocess
from pathlib import Path

# datasets 폴더 경로
base_dir = Path("/mnt/c/Users/PC012/Desktop/BCE/HEVC_32/datasets")

# 처리할 dataset 폴더 이름
dataset_names = ["1_bicycle"]

for name in dataset_names:
    dataset_path = base_dir / name
    image_path = dataset_path / "images"
    sparse_path = dataset_path / "sparse"

    db_path = sparse_path / "database.db"

    # sparse 폴더 생성
    sparse_path.mkdir(parents=True, exist_ok=True)

    # 1) 특징점 추출 (feature 안정화 옵션 추가)
    subprocess.run([
        "colmap", "feature_extractor",
        "--database_path", str(db_path),
        "--image_path", str(image_path),
        "--ImageReader.camera_model", "SIMPLE_PINHOLE",
        "--SiftExtraction.peak_threshold", "0.03",   # 기본 0.02 → 높이면 불안정 feature 감소
        "--SiftExtraction.edge_threshold", "15"      # 기본 10 → 강한 edge 위주 feature
    ], check=True)

    # 2) 이미지 간 매칭
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", str(db_path)
    ], check=True)

    # 3) SfM (sparse reconstruction) 안정화 옵션 적용
    subprocess.run([
        "colmap", "mapper",
        "--database_path", str(db_path),
        "--image_path", str(image_path),
        "--output_path", str(sparse_path),
        "--Mapper.min_num_inliers", "50",         # triangulation 최소 inlier 수
        "--Mapper.init_min_tri_angle", "4"       # 초기 triangulation 최소 각도
    ], check=True)

    print(f"[INFO] Dataset {name} processed with SfM stabilization.")
