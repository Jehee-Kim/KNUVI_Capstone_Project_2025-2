import random
import re
from pathlib import Path
from PIL import Image
import pillow_heif
from pillow_heif import register_heif_opener

# HEIC 지원 등록
register_heif_opener()

# 입력 루트 디렉토리
root_dir = Path("C:/Users/PC016/Desktop/Blind_images_v2")

# 지원 코덱
formats = {
    "JPEG": "jpg",
    "JPEG2000": "jp2",
    "HEIC": "heic"
}

# 정규식 패턴: 숫자_숫자_숫자
seq_pattern = re.compile(r"^\d+_\d+_\d+$")

# category level 순회
for category_dir in root_dir.iterdir():
    if not category_dir.is_dir() or category_dir.name.startswith('.'):
        continue

    for seq_dir in category_dir.iterdir():
        if not seq_dir.is_dir() or seq_dir.name.startswith('.'):
            continue
        if not seq_pattern.match(seq_dir.name):
            continue

        images_dir = seq_dir / "images"
        if not images_dir.is_dir():
            continue

        images = sorted([f for f in images_dir.glob("*") 
                         if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]
                         and not f.name.startswith('.')])
        if not images:
            continue

        n_frames = len(images)

        # 압축 저장 루트
        compressed_root = seq_dir / "compressed"
        compressed_root.mkdir(parents=True, exist_ok=True)

        # --- 코덱 분배 리스트 만들기 ---
        base = n_frames // len(formats)      # 기본 개수
        remainder = n_frames % len(formats)  # 나머지

        codec_list = []
        for i, codec in enumerate(formats.keys()):
            count = base + (1 if i < remainder else 0)
            codec_list.extend([codec] * count)

        random.shuffle(codec_list)  # 섞어서 랜덤 분배

        # --- 저장 ---
        for idx, img_file in enumerate(images, start=1):
            try:
                img = Image.open(img_file).convert("RGB")

                codec = codec_list[idx-1]
                ext = formats[codec]
                q = random.randint(10, 100)

                out_file = compressed_root / f"frame{idx:06d}_{codec}_Q{q}.{ext}"

                if codec == "HEIC":
                    heif_file = pillow_heif.from_pillow(img)
                    heif_file.save(out_file, quality=q)
                else:
                    img.save(out_file, format=codec, quality=q)

                print(f"{seq_dir.name} frame {idx:06d} → {codec} (Q={q})")

            except Exception as e:
                print(f"Error processing {img_file}: {e}")

        # 분포 확인용 출력
        summary = {c: codec_list.count(c) for c in formats.keys()}
        print(f"✅ Finished set {category_dir.name}/{seq_dir.name}: {summary}")
