import os
import re
import subprocess
import pathlib

base_dir = "/Users/jehee/Documents/KNU/intern/Blind_images_v2"
output_base = "/Users/jehee/Documents/KNU/intern/Blind_images_v2/avc"
category_list = ["backpack", "ball", "book", "bottle", "chair", "cup", "handbag", "labtop", "plant", "teddybear", "vase"]   # 필요한 카테고리

qp_list = [27, 32, 37]

# 숫자_숫자_숫자 폴더 정규식
pattern = re.compile(r"^\d+_\d+_\d+$")

for qp in qp_list:
    for category in category_list:
        category_path = os.path.join(base_dir, category)
        if not os.path.isdir(category_path):
            continue

        for subfolder in os.listdir(category_path):
            if not pattern.match(subfolder):
                continue

            image_dir = os.path.join(category_path, subfolder, "images")
            if not os.path.isdir(image_dir):
                continue

            # 입력 프레임 리스트
            files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(".jpg")])
            if not files:
                continue

            # 임시 영상 파일
            temp_video = os.path.join(output_base, category, f"{subfolder}_qp{qp}.mp4")
            os.makedirs(os.path.dirname(temp_video), exist_ok=True)

            # 출력 프레임 폴더
            output_frames_dir = os.path.join(output_base, category, subfolder, f"images_qp{qp}")
            os.makedirs(output_frames_dir, exist_ok=True)

            # 1. 영상 만들기 (QP 고정, B=2)
            cmd_compress = [
                "ffmpeg", "-y",
                "-framerate", "30",
                "-i", os.path.join(image_dir, "frame%06d.jpg"),
                "-vf", "pad=ceil(iw/2)*2:ceil(ih/2)*2",
                "-c:v", "libx264",
                "-profile:v", "high",
                "-preset", "slow",
                "-qp", str(qp),
                "-x264-params", "bframes=2:keyint=48:scenecut=0",
                "-pix_fmt", "yuv420p",
                temp_video
            ]
            subprocess.run(cmd_compress, check=True)

            # 2. 영상 → PNG 프레임 추출
            # 이름은 {원래파일명}_AVCRA_{QP}.png
            cmd_extract = [
                "ffmpeg", "-y",
                "-i", temp_video,
                os.path.join(output_frames_dir, f"frame_%06d.png")
            ]
            subprocess.run(cmd_extract, check=True)

            # 파일명 변환 (frame_000001.png → {원래파일명}_AVCRA_{qp}.png)
            for idx, file in enumerate(files, start=1):
                orig_stem = pathlib.Path(file).stem
                src = os.path.join(output_frames_dir, f"frame_{idx:06d}.png")
                dst = os.path.join(output_frames_dir, f"{orig_stem}_AVCRA_{qp}.png")
                if os.path.exists(src):
                    os.rename(src, dst)

            print(f"✅ {category}/{subfolder} QP={qp} 완료 → {output_frames_dir}")
