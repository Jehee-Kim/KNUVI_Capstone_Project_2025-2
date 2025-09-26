import os
from PIL import Image
import pathlib
import re

# ✅ 사용자가 직접 설정하는 부분
base_dir = "/Users/jehee/Documents/KNU/intern/Blind_images_v2"   # 원본 데이터 경로
output_base = "/Users/jehee/Documents/KNU/intern/Blind_images_v2/jpeg"                          # 결과 저장 경로
category_list = ["backpack", "ball", "book", "bottle", "chair", "cup", "handbag", "labtop", "plant", "teddybear", "vase"]                     # 필요한 카테고리만 선택
jpeg_quality_list = [30, 50, 70]                         # JPEG 품질 리스트

# 숫자_숫자_숫자 폴더 매칭 정규식
pattern = re.compile(r"^\d+_\d+_\d+$")

for jpeg_quality in jpeg_quality_list:
    # 품질별 아웃풋 폴더 생성
    output_dir = os.path.join(output_base, f"JpegOutput_{jpeg_quality}")
    os.makedirs(output_dir, exist_ok=True)

    for category in category_list:
        category_path = os.path.join(base_dir, category)
        if not os.path.isdir(category_path):
            print(f"⚠️ 카테고리 {category_path} 없음. 건너뜀.")
            continue

        # category 안에서 숫자_숫자_숫자 폴더만 탐색
        for subfolder in os.listdir(category_path):
            if not pattern.match(subfolder):
                continue  # 패턴 안 맞으면 무시

            image_dir = os.path.join(category_path, subfolder, "images")
            if not os.path.isdir(image_dir):
                print(f"⚠️ {image_dir} 없음. 건너뜀.")
                continue

            # 출력 폴더 구조 동일하게 생성
            output_subdir = os.path.join(output_dir, category, subfolder, "images")
            os.makedirs(output_subdir, exist_ok=True)

            # 이미지 처리
            files = [f for f in os.listdir(image_dir) if f.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff"))]
            if not files:
                print(f"⚠️ {image_dir} 에 이미지 없음.")
                continue

            for file in files:
                img_path = os.path.join(image_dir, file)
                try:
                    with Image.open(img_path) as img:
                        if img.mode != "RGB":
                            img = img.convert("RGB")

                        # 저장 파일명 = 원래이름 + _JPEG_Q{품질}
                        stem = pathlib.Path(file).stem
                        save_name = f"{stem}_JPEG_Q{jpeg_quality}.jpg"
                        save_path = os.path.join(output_subdir, save_name)

                        img.save(save_path, "JPEG", quality=jpeg_quality, optimize=True)
                        print(f"[{category}/{subfolder}] [Q={jpeg_quality}] ✅ {save_name}")
                except Exception as e:
                    print(f"❌ {img_path} 오류: {e}")

    print(f"🎉 JPEG Quality={jpeg_quality} 완료! 결과는 {output_dir} 에 저장됨\n")

print("✅ 모든 품질 버전 압축 완료!")
