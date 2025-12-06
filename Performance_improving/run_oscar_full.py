import os
import subprocess
import numpy as np
import csv
from imageio import imread
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
import torch
import lpips

# ======================
# LPIPS 모델 초기화
# ======================
device = 'cuda' if torch.cuda.is_available() else 'cpu'
lpips_alex = lpips.LPIPS(net='alex').to(device).eval()


# ======================
# 단일 이미지 지표 계산
# ======================
def calc_image_metrics(gt_img, pred_img):

    if gt_img.ndim == 2:
        gt_img = np.stack([gt_img]*3, axis=-1)
    if pred_img.ndim == 2:
        pred_img = np.stack([pred_img]*3, axis=-1)

    if gt_img.shape[2] == 4:
        gt_img = gt_img[:, :, :3]
    if pred_img.shape[2] == 4:
        pred_img = pred_img[:, :, :3]

    gt = gt_img.astype(np.float32) / 255.0
    pr = pred_img.astype(np.float32) / 255.0

    if gt.shape != pr.shape:
        pr = resize(pr, gt.shape, preserve_range=True, anti_aliasing=True)
        pr = np.clip(pr, 0.0, 1.0)

    psnr_val = psnr(gt, pr, data_range=1.0)
    ssim_val = ssim(gt, pr, data_range=1.0, channel_axis=2, win_size=7)

    gt_t = torch.from_numpy(gt).permute(2, 0, 1).unsqueeze(0).float().to(device)
    pr_t = torch.from_numpy(pr).permute(2, 0, 1).unsqueeze(0).float().to(device)

    gt_t = gt_t * 2 - 1
    pr_t = pr_t * 2 - 1

    with torch.no_grad():
        lpips_val = lpips_alex(gt_t, pr_t).item()

    return psnr_val, ssim_val, lpips_val


# ======================
# 폴더 단위 지표 계산 (GT를 pred 크기로 맞출 수 있도록 수정)
# ======================
def calc_folder_metrics(gt_dir, pred_dir, resize_gt=False):

    files = sorted([
        f for f in os.listdir(gt_dir)
        if f.lower().endswith(("png", "jpg", "jpeg")) and not f.startswith("._")
    ])

    psnr_list, ssim_list, lpips_list = [], [], []

    for f in files:
        gt_path = os.path.join(gt_dir, f)
        pred_path = os.path.join(pred_dir, f)
        if not os.path.exists(pred_path):
            continue

        gt_img = imread(gt_path)
        pr_img = imread(pred_path)

        # ★ AFTER 평가일 경우: GT를 pred 해상도로 resize
        if resize_gt:
            H, W = pr_img.shape[:2]
            gt_img = resize(gt_img, (H, W), preserve_range=True, anti_aliasing=True)
            gt_img = np.clip(gt_img, 0, 255).astype(np.uint8)

        ps, ss, lp = calc_image_metrics(gt_img, pr_img)
        psnr_list.append(ps)
        ssim_list.append(ss)
        lpips_list.append(lp)

    return np.mean(psnr_list), np.mean(ssim_list), np.mean(lpips_list)


# ======================
# OSCAR 수행 + 정량 평가
# ======================
def run_oscar_case(case_name, input_dir, gt_dir, writer):
    output_dir = f"output{case_name}"
    print(f"\n=== Running OSCAR on {input_dir} → {output_dir} ===")

    subprocess.run([
        "python3", "main_test.py",
        "--input_image", input_dir,
        "--output_dir", output_dir,
        "--pretrained_model_name_or_path", "model_zoo/stable-diffusion-2-1",
        "--oscar_path", "model_zoo/oscar.pkl"
    ], check=True)

    # BEFORE: GT와 입력 JPEG는 동일 해상도 → resize 불필요
    metrics_before = calc_folder_metrics(gt_dir, input_dir, resize_gt=False)
    print(f" → JPEG{case_name} BEFORE: PSNR {metrics_before[0]:.4f}, "
          f"SSIM {metrics_before[1]:.4f}, LPIPS {metrics_before[2]:.4f}")

    range_folders = sorted([
        d for d in os.listdir(output_dir)
        if os.path.isdir(os.path.join(output_dir, d))
    ])

    best_psnr = -1
    best_folder = None
    best_metrics = None

    for rf in range_folders:
        pred_dir = os.path.join(output_dir, rf)
        try:
            # ★ AFTER: pred 크기에 GT를 맞춰서 평가해야 함
            metrics_after = calc_folder_metrics(gt_dir, pred_dir, resize_gt=True)

            is_best = False
            if metrics_after[0] > best_psnr:
                best_psnr = metrics_after[0]
                best_folder = rf
                best_metrics = metrics_after
                is_best = True

            writer.writerow([
                case_name, rf,
                round(metrics_before[0], 4),
                round(metrics_before[1], 4),
                round(metrics_before[2], 4),
                round(metrics_after[0], 4),
                round(metrics_after[1], 4),
                round(metrics_after[2], 4),
                is_best
            ])

            print(f"    Range {rf} → PSNR {metrics_after[0]:.4f}, "
                  f"SSIM {metrics_after[1]:.4f}, LPIPS {metrics_after[2]:.4f}")

        except Exception as e:
            print(f"    Skip {rf}: {e}")
            continue

    print(f" → JPEG{case_name} BEST folder: {best_folder}, "
          f"PSNR {best_metrics[0]:.4f}, SSIM {best_metrics[1]:.4f}, "
          f"LPIPS {best_metrics[2]:.4f}")

    return metrics_before, best_metrics


# ======================
# 메인 실행
# ======================
if __name__ == "__main__":

    os.chdir("OSCAR")

    cases = [
        ("10", "../jpeg10", "../gt_for_jpeg10"),
        ("50", "../jpeg50", "../gt"),
        ("70", "../jpeg70", "../gt")
    ]

    results = {}
    csv_file = "oscar_metrics_all_ranges.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "JPEG", "range",
            "PSNR_before", "SSIM_before", "LPIPS_before",
            "PSNR_after", "SSIM_after", "LPIPS_after",
            "is_best"
        ])

        for case_name, inp, gt in cases:
            metrics_before, metrics_after = run_oscar_case(case_name, inp, gt, writer)
            results[case_name] = (metrics_before, metrics_after)

    print(f"\nAll results saved to {csv_file}")
