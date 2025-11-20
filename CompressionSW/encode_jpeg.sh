import os
from PIL import Image
import pathlib

# ✅ 사용자 설정
base_root = "/Volumes/T7/experiments/Mip-NeRF360"   # 카테고리들이 들어있는 루트 경로
output_root = "/Volumes/T7/experiments/Mip-NeRF360_JPEG8"  # 전체 결과 저장 루트 경로

# 여러 JPEG 압축 품질 (1 ~ 95 권장)
jpeg_quality_list = [10, 30, 50, 70, 90]

# base_root 하위 카테고리 탐색 (예: bicycle, garden, room …)
categories = [d for d in os.listdir(base_root) if os.path.isdir(os.path.join(base_root, d))]

for category in categories:
    category_path = os.path.join(base_root, category)
    images_path = os.path.join(category_path, "images_8")
    if not os.path.isdir(images_path):
        print(f"⚠️ {images_path} 가 존재하지 않습니다. 건너뜁니다.")
        continue

    for jpeg_quality in jpeg_quality_list:
        # 품질별 아웃풋 폴더 생성
        output_dir = os.path.join(output_root, f"JpegOutput_{jpeg_quality}", category, "images_8")
        os.makedirs(output_dir, exist_ok=True)

        # 이미지 파일 수집
        files = [f for f in os.listdir(images_path) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff"))]
        if not files:
            print(f"⚠️ {images_path} 에 이미지 파일이 없습니다.")
            continue

        for file in files:
            img_path = os.path.join(images_path, file)
            try:
                with Image.open(img_path) as img:
                    if img.mode != "RGB":
                        img = img.convert("RGB")

                    # 원래 파일명 + _{quality}.jpg
                    stem = pathlib.Path(file).stem
                    save_name = f"{stem}_{jpeg_quality}.jpg"
                    save_path = os.path.join(output_dir, save_name)

                    img.save(save_path, "JPEG", quality=jpeg_quality, optimize=True)
                    print(f"[{category}] [Q={jpeg_quality}] ✅ 저장 완료: {save_path}")
            except Exception as e:
                print(f"❌ {img_path} 처리 중 오류: {e}")

        print(f"🎉 카테고리={category}, JPEG Quality={jpeg_quality} 처리 완료! 결과는 {output_dir} 에 저장됨\n")

print("✅ 모든 카테고리/품질 버전 압축 완료!")
