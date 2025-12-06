import cv2
import numpy as np
import os

# 패딩 적용할 폴더 리스트
folders = ["gt", "gt_for_jpeg10", "jpeg10", "jpeg50", "jpeg70"]

for folder in folders:
    if not os.path.exists(folder):
        print(f"{folder} 폴더가 존재하지 않습니다. 건너뜁니다.")
        continue

    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path)

            if img is None:
                print(f"{img_path} 읽기 실패")
                continue

            h, w = img.shape[:2]

            # 128 배수로 올림
            new_h = ((h + 127) // 128) * 128
            new_w = ((w + 127) // 128) * 128

            pad_bottom = new_h - h
            pad_right = new_w - w

            # 하단과 오른쪽에 패딩
            padded_img = cv2.copyMakeBorder(img, 0, pad_bottom, 0, pad_right,
                                            borderType=cv2.BORDER_CONSTANT, value=[0,0,0])

            # 원본 덮어쓰기
            cv2.imwrite(img_path, padded_img)

print("모든 이미지 128배수 패딩 완료! (원본 덮어쓰기)")
