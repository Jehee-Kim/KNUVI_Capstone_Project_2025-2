import os
import csv
from plyfile import PlyData
from statistics import mean
from collections import defaultdict

# === 기본 경로 설정 ===
BASE_PATH = "/home/knuvi/vggtoutput/Blind_images_v2"
OUTPUT_DIR = "/home/knuvi/Points_summary"
os.makedirs(OUTPUT_DIR, exist_ok=True)  # 결과 저장 폴더 자동 생성

# === 처리할 코덱별 QP 설정 ===
QP_MAP = {
    "avc": [27, 32, 37, 42, 47],
    "jpeg": [10, 20, 30, 50, 70]
}

# === 처리할 카테고리 목록 ===
CATEGORIES = ["backpack", "ball", "book", "chair", "handbag", "laptop", "plant", "teddybear", "vase"]

results = []

for codec, qp_list in QP_MAP.items():
    for qp in qp_list:
        qp_folder = f"output_AVCRA{qp}" if codec == "avc" else f"output_JPEG{qp}"
        qp_path = os.path.join(BASE_PATH, codec, qp_folder)
        if not os.path.isdir(qp_path):
            print(f"⚠️ Skip: {qp_path} (not found)")
            continue

        for category in CATEGORIES:
            category_folder = f"output_{category}"
            category_path = os.path.join(qp_path, category_folder)
            if not os.path.isdir(category_path):
                print(f"⚠️ Missing category folder: {category_path}")
                continue

            # frame 폴더만 필터링
            frame_folders = sorted([
                f for f in os.listdir(category_path)
                if f.startswith("frame") and os.path.isdir(os.path.join(category_path, f))
            ])

            if not frame_folders:
                print(f"⚠️ No frame folders found in {category_path}")
                continue

            for i, frame_folder in enumerate(frame_folders):
                #if i % 5 != 0:
                #    continue

                ply_path = os.path.join(category_path, frame_folder, "points.ply")
                if os.path.exists(ply_path):
                    try:
                        plydata = PlyData.read(ply_path)
                        num_points = len(plydata["vertex"])
                        results.append({
                            "codec": codec,
                            "qp": qp,
                            "category": category,
                            "frame": frame_folder,
                            "num_points": num_points
                        })
                    except Exception as e:
                        print(f"❌ Error reading {ply_path}: {e}")
                else:
                    print(f"⚠️ Missing file: {ply_path}")

# === CSV 저장 (frame 단위) ===
frame_csv = os.path.join(OUTPUT_DIR, "points_summary.csv")
with open(frame_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["codec", "qp", "category", "frame", "num_points"])
    writer.writeheader()
    writer.writerows(results)

# === 평균 계산 ===
cat_mean = defaultdict(list)
qp_mean = defaultdict(list)

for r in results:
    cat_mean[r["category"]].append(r["num_points"])
    qp_mean[(r["codec"], r["qp"])].append(r["num_points"])

# === 평균 CSV 따로 저장 ===
mean_csv = os.path.join(OUTPUT_DIR, "points_summary_means.csv")
with open(mean_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["type", "codec", "qp", "category", "mean_num_points"])

    # 카테고리 평균
    for cat, vals in cat_mean.items():
        writer.writerow(["category", "", "", cat, mean(vals)])

    # QP 평균
    for (codec, qp), vals in qp_mean.items():
        writer.writerow(["qp", codec, qp, "", mean(vals)])

print(f"✅ Done!")
print(f"📄 Frame-level CSV: {frame_csv}")
print(f"📄 Mean summary CSV: {mean_csv}")
