
import os
import re
import glob
import torch
import lpips
import numpy as np
from PIL import Image
import torchvision.transforms.functional as TF
import torch.nn.functional as F
import pandas as pd

# ======================
# 경로 설정
# ======================
GT_ROOT = "/home/knuvi/dataset/Blind_images_v123"
AVC_ROOT = "/home/knuvi/dataset/Blind_images_v2/avc"
JPEG_ROOT = "/home/knuvi/dataset/Blind_images_v2/jpeg"
SAVE_CSV = "/home/knuvi/results/psnr_lpips_summary_AVC.csv"

# ======================
# 설정
# ======================
CATEGORIES = ["backpack", "ball", "book", "chair", "handbag", "laptop", "plant", "teddybear", "vase"]
AVC_QPS = [27, 32, 37, 42, 47]
JPEG_QPS = [70, 50, 30, 20, 10]

# ======================
# 유틸 함수
# ======================
def calculate_psnr(img1, img2):
    mse = F.mse_loss(img1, img2)
    if mse == 0:
        return float("inf")
    return 20 * torch.log10(1.0 / torch.sqrt(mse))

def load_image(path, device):
    img = Image.open(path).convert("RGB")
    tensor = TF.to_tensor(img).unsqueeze(0).to(device)
    return tensor

def get_dpattern_folders(root):
    #폴더 이름이 d+_d+_d+ 형태인 것만 선택
    return [
        os.path.join(root, f)
        for f in os.listdir(root)
        if re.match(r"^\d+_\d+_\d+$", f)
    ]

# ======================
# 디바이스 설정
# ======================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🚀 Using device: {device}")

# LPIPS 모델 초기화 (GPU로 이동)
lpips_fn = lpips.LPIPS(net='alex').to(device)
lpips_fn.eval()

# ======================
# 계산
# ======================
results = []

for category in CATEGORIES:
    gt_category_path = os.path.join(GT_ROOT, category)
    if not os.path.isdir(gt_category_path):
        print(f"[경고] 카테고리 없음: {gt_category_path}")
        continue

    seq_folders = get_dpattern_folders(gt_category_path)
    if not seq_folders:
        print(f"[경고] {category} 내에 유효한 시퀀스 폴더 없음")
        continue

    for codec, qps in [("avc", AVC_QPS)]:
    #for codec, qps in [("jpeg", JPEG_QPS)]:
        for qp in qps:
            psnr_vals, lpips_vals = [], []

            print(f"\n==== {category} / {codec.upper()} QP{qp} ====")
            for seq_path in seq_folders:
                seq_name = os.path.basename(seq_path)
                gt_imgs = sorted(glob.glob(os.path.join(seq_path, "images", "frame*.png")))

                if len(gt_imgs) == 0:
                    print(f"❌ GT 이미지 없음: {seq_path}")
                    continue

                # 압축본 경로
                if codec == "avc":
                    comp_dir = os.path.join(AVC_ROOT, category, seq_name, f"images_qp{qp}")
                    comp_ext = f"_AVCRA_{qp}.png"
                else:
                    comp_dir = os.path.join(JPEG_ROOT, f"JpegOutput_{qp}", category, seq_name, "images")
                    comp_ext = f"_JPEG_Q{qp}.jpg"

                if not os.path.isdir(comp_dir):
                    print(f"❌ 압축 이미지 폴더 없음: {comp_dir}")
                    continue

                comp_imgs = sorted(glob.glob(os.path.join(comp_dir, f"frame*{comp_ext}")))
                if len(comp_imgs) == 0:
                    print(f"❌ 압축 이미지 없음: {comp_dir}")
                    continue

                gt_frames = {os.path.basename(p).split(".")[0]: p for p in gt_imgs}
                comp_frames = {
                    os.path.basename(p).replace(comp_ext, ""): p
                    for p in comp_imgs
                }

                common_frames = sorted(set(gt_frames.keys()) & set(comp_frames.keys()))
                print(f"📂 {seq_name}: GT={len(gt_imgs)}, COMP={len(comp_imgs)}, 교집합={len(common_frames)}")

                if not common_frames:
                    continue

                for frame_name in common_frames:
                    gt_path = gt_frames[frame_name]
                    comp_path = comp_frames[frame_name]

                    gt_img = load_image(gt_path, device)
                    comp_img = load_image(comp_path, device)
                    if gt_img.shape != comp_img.shape:
                        print(f"⚠️ 크기 불일치: {gt_path}")
                        continue

                    with torch.no_grad():
                        psnr = calculate_psnr(gt_img, comp_img).item()
                        lp = lpips_fn(gt_img, comp_img).item()

                    psnr_vals.append(psnr)
                    lpips_vals.append(lp)

            if len(psnr_vals) == 0:
                print(f"[{codec.upper()} QP{qp}] {category} - 비교할 이미지 없음 🚫")
                continue

            psnr_mean = np.mean(psnr_vals)
            lpips_mean = np.mean(lpips_vals)
            results.append([codec.upper(), qp, category, psnr_mean, lpips_mean])
            print(f"✅ [{codec.upper()} QP{qp}] {category}: PSNR={psnr_mean:.2f}, LPIPS={lpips_mean:.4f}")

# ======================
# 전체 평균 계산 + 저장
# ======================
if results:
    df = pd.DataFrame(results, columns=["Codec", "QP", "Category", "PSNR", "LPIPS"])
    total_df = (
        df.groupby(["Codec", "QP"], as_index=False)
        .agg({"PSNR": "mean", "LPIPS": "mean"})
        .assign(Category="ALL_AVG")
    )
    df = pd.concat([df, total_df], ignore_index=True)
    os.makedirs(os.path.dirname(SAVE_CSV), exist_ok=True)
    df.to_csv(SAVE_CSV, index=False)
    print(f"\n✅ 결과 저장 완료: {SAVE_CSV}")
else:
    print("⚠️ 비교 가능한 결과가 없습니다.")
