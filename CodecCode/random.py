import random
from pathlib import Path
from PIL import Image
import pillow_heif
from pillow_heif import register_heif_opener

# HEIC 지원 등록
register_heif_opener()

# 입력/출력 디렉토리
root_dir = Path("/Volumes/T7/co3d/single_sequence_subset")
output_root = Path("/Volumes/T7/co3d/RandomOutput")

# 지원 코덱 
formats = {
    "JPEG": "jpg",
    "JPEG2000": "jp2",
    "HEIC": "heic"
}

# category/apple/.../images 구조 순회
for category_dir in root_dir.iterdir():
    if category_dir.is_dir() and not category_dir.name.startswith('.'):
        category = category_dir.name

        for seq_dir in category_dir.iterdir():
            if not seq_dir.name.startswith('.'):
                images_dir = seq_dir / "images"
                if images_dir.is_dir():
                    images = sorted([f for f in images_dir.glob("*") 
                                     if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"] 
                                     and not f.name.startswith('.')])
                    if not images:
                        continue

                    # 한 세트에 대해 codec, quality 하나 랜덤 선택
                    codec = random.choice(list(formats.keys()))
                    ext = formats[codec]
                    quality = random.randint(10, 100)

                    # 출력 경로
                    out_dir = output_root / category / seq_dir.name / f"{codec}_{quality}"
                    out_dir.mkdir(parents=True, exist_ok=True)

                    # 모든 이미지 저장 (1부터 시작)
                    for idx, img_file in enumerate(images, start=1):
                        try:
                            img = Image.open(img_file).convert("RGB")
                            out_file = out_dir / f"frame_{idx:03d}.{ext}"
                            
                            if codec == "HEIC" :
                                heif_file = pillow_heif.from_pillow(img)
                                heif_file.save(out_file, quality=quality)
                            else :
                                img.save(out_file, format=codec, quality=quality)

                            print(f"Saved: {out_file} (codec={codec}, Q={quality})")
                        except Exception as e:
                            print(f"Error processing {img_file}: {e}")

                    print(f"Finished set {category}/{seq_dir.name} -> {codec}_{quality} ({len(images)} frames)\n")
