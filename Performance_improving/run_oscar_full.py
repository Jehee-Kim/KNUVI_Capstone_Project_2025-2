import os
import subprocess
import numpy as np
from imageio import imread
from skimage.metrics import peak_signal_noise_ratio as psnr

# ======================
# 폴더 단위 PSNR 계산 함수
# ======================
def calc_folder_psnr(gt_dir, pred_dir):
    # GT 폴더의 정상 이미지들만 선택
    files = sorted([
        f for f in os.listdir(gt_dir)
        if f.lower().endswith(("png", "jpg", "jpeg")) and not f.startswith("._")
    ])

    psnr_list = []
    for f in files:
        gt = imread(os.path.join(gt_dir, f))
        pr = imread(os.path.join(pred_dir, f))
        psnr_list.append(psnr(gt, pr, data_range=255))

    return float(np.mean(psnr_list))


# ===============================================
# 여러 range 폴더 중 GT와 가장 PSNR 높은 폴더 찾기
# ===============================================
def find_best_range_folder(gt_dir, pred_base_dir):
    range_folders = sorted([
        d for d in os.listdir(pred_base_dir)
        if os.path.isdir(os.path.join(pred_base_dir, d))
    ])

    best_psnr = -1
    best_folder = None

    for rf in range_folders:
        pred_dir = os.path.join(pred_base_dir, rf)

        # 이미지 폴더가 아닌 경우 스킵
        if not os.path.isdir(pred_dir):
            continue

        try:
            score = calc_folder_psnr(gt_dir, pred_dir)
            print(f"    Range {rf} → PSNR {score:.4f} dB")  # 각 폴더 PSNR 출력

            if score > best_psnr:
                best_psnr = score
                best_folder = pred_dir

        except Exception as e:
            print(f"    Skip {rf}: {e}")
            continue

    return best_folder, best_psnr


# ===============================================
# OSCAR 실행 (한 케이스에 대해)
# ===============================================
def run_oscar_case(case_name, input_dir, gt_dir):
    output_dir = f"output{case_name}"

    print(f"\n=== Running OSCAR on {input_dir} → {output_dir} ===")

    # main_test.py 실행 (전체 디렉토리 넣기)
    subprocess.run([
        "python3", "main_test.py",
        "--input_image", input_dir,
        "--output_dir", output_dir,
        "--pretrained_model_name_or_path", "model_zoo/stable-diffusion-2-1",
        "--oscar_path", "model_zoo/oscar.pkl"
    ], check=True)

    # 입력 PSNR 계산
    psnr_before = calc_folder_psnr(gt_dir, input_dir)

    # 출력 range 폴더 중 가장 좋은 결과 찾기
    best_folder, psnr_after = find_best_range_folder(gt_dir, output_dir)

    print(f"\n → JPEG{case_name} before: {psnr_before:.4f} dB")
    print(f" → JPEG{case_name} best after: {psnr_after:.4f} dB")
    print(f" → Best folder: {best_folder}")

    return psnr_before, psnr_after


# ===============================================
# 메인 실행
# ===============================================
if __name__ == "__main__":
    os.chdir("OSCAR")  # test/OSCAR 디렉토리로 이동

    cases = [
        ("10", "../jpeg10", "../gt_for_jpeg10"),
        ("50", "../jpeg50", "../gt"),
        ("70", "../jpeg70", "../gt")
    ]

    results = {}
    for case_name, inp, gt in cases:
        results[case_name] = run_oscar_case(case_name, inp, gt)

    print("\n================ Summary ================")
    for k, (b, a) in results.items():
        print(f"JPEG{k} → before: {b:.4f} dB | after: {a:.4f} dB")
