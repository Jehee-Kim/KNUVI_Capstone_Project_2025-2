db_path = colmap_output / "database.db"
sparse_path = colmap_output / "sparse"

# sparse 폴더 생성
sparse_path.mkdir(parents=True, exist_ok=True)

# 1) 특징점 추출
subprocess.run([
    "colmap", "feature_extractor",
    "--database_path", str(db_path),
    "--image_path", str(image_path),
    "--ImageReader.camera_model", "SIMPLE_PINHOLE"
], check=True)

# 2) 이미지 간 매칭
subprocess.run([
    "colmap", "exhaustive_matcher",
    "--database_path", str(db_path)
], check=True)

# 3) SfM (sparse reconstruction)
subprocess.run([
    "colmap", "mapper",
    "--database_path", str(db_path),
    "--image_path", str(image_path),
    "--output_path", str(sparse_path)
], check=True)

print(f"[INFO] Dataset {name} processed.")
