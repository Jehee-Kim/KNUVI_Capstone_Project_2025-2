cd "/mnt/c/Users/PC012/Desktop/original_HEVC_42/original_HEVC copy/1_bicycle/test/ours_30000/gt"

for f in *.JPG; do
    ffmpeg -y -i "$f" -vf "crop=618:410:0:0" "${f%.JPG}.png"
    rm "$f"  # 변환 후 원본 JPG 삭제
done
cd "/mnt/c/Users/PC012/Desktop/original_HEVC_42/original_HEVC copy/6_kitchen/test/ours_30000/gt"

for f in *.JPG; do
    ffmpeg -y -i "$f" -vf "crop=388:260:0:0" "${f%.JPG}.png"
    rm "$f"
done
cd "/mnt/c/Users/PC012/Desktop/original_HEVC_42/original_HEVC copy/7_room/test/ours_30000/gt"

for f in *.JPG; do
    ffmpeg -y -i "$f" -vf "crop=388:258:0:0" "${f%.JPG}.png"
    rm "$f"
done
