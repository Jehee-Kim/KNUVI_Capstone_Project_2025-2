import os
import re
import csv
import numpy as np
import open3d as o3d
import torch

# -----------------------------
# Chamfer Distance (GPU, 메모리 안전)
# -----------------------------
def chamfer_distance(P, Q, squared=True, symmetric=True, batch_size=1000):
    """
    P, Q: numpy arrays [N,3], [M,3]
    batch_size: 한번에 처리할 포인트 수 (GPU 메모리 조절)
    """
    if P is None or Q is None or len(P) == 0 or len(Q) == 0:
        return None

    P = torch.tensor(P, dtype=torch.float32, device="cuda")
    Q = torch.tensor(Q, dtype=torch.float32, device="cuda")

    N, M = P.shape[0], Q.shape[0]

    # --- P -> Q ---
    min_dists_P = []
    for i in range(0, N, batch_size):
        P_batch = P[i:i+batch_size]  # [B,3]
        dists = torch.cdist(P_batch.unsqueeze(0), Q.unsqueeze(0), p=2).squeeze(0)  # [B,M]
        min_dists, _ = dists.min(dim=1)
        min_dists_P.append(min_dists)
    min_dists_P = torch.cat(min_dists_P)
    term_P = (min_dists_P**2).mean() if squared else min_dists_P.mean()

    if not symmetric:
        return term_P.item()

    # --- Q -> P ---
    min_dists_Q = []
    for j in range(0, M, batch_size):
        Q_batch = Q[j:j+batch_size]  # [B,3]
        dists = torch.cdist(Q_batch.unsqueeze(0), P.unsqueeze(0), p=2).squeeze(0)  # [B,N]
        min_dists, _ = dists.min(dim=1)
        min_dists_Q.append(min_dists)
    min_dists_Q = torch.cat(min_dists_Q)
    term_Q = (min_dists_Q**2).mean() if squared else min_dists_Q.mean()

    return (term_P + term_Q).item()

# -----------------------------
# PLY 파일 로드
# -----------------------------
def load_ply(path):
    if not os.path.exists(path):
        return None
    pcd = o3d.io.read_point_cloud(path)
    return np.asarray(pcd.points)

# -----------------------------
# Chamfer Distance 평가 공통 함수
# -----------------------------
def evaluate_codec(gt_base, out_base, codec_name, codec_pattern, categories, qps):
    dir_pattern = re.compile(r"^\d+_\d+_\d+$")

    frame_csv = f"chamfer_{codec_name}_frame3.csv"
    avg_csv = f"chamfer_{codec_name}_avg3.csv"

    if os.path.exists(frame_csv): os.remove(frame_csv)
    if os.path.exists(avg_csv): os.remove(avg_csv)

    frame_results, avg_results = [], []

    for category in categories:
        gt_category_dir = os.path.join(gt_base, category)
        for subdir in os.listdir(gt_category_dir):
            if not dir_pattern.match(subdir):
                continue

            gt_ply_path = os.path.join(gt_category_dir, subdir, "pointcloud.ply")
            if not os.path.exists(gt_ply_path):
                continue
            gt_points = load_ply(gt_ply_path)
            if gt_points is None or len(gt_points) == 0:
                continue

            qp_list = qps if qps else [None]
            for qp in qp_list:
                out_dir = codec_pattern.format(base=out_base, qp=qp, category=category)
                if not os.path.exists(out_dir):
                    continue

                frame_dirs = sorted(
                    [d for d in os.listdir(out_dir) if os.path.isdir(os.path.join(out_dir, d))]
                )

                cds = []
                for frame in frame_dirs:
                    ply_path = os.path.join(out_dir, frame, "points.ply")
                    if not os.path.exists(ply_path):
                        continue
                    out_points = load_ply(ply_path)
                    if out_points is None or len(out_points) == 0:
                        continue

                    cd = chamfer_distance(gt_points, out_points, squared=True, symmetric=True, batch_size=1000)
                    if cd is None:
                        continue
                    cds.append(cd)

                    frame_results.append({
                        "codec": codec_name,
                        "category": category,
                        "qp": qp if qp is not None else "N/A",
                        "frame": frame,
                        "chamfer_distance": cd
                    })
                    print(f"[FRAME] {codec_name} | {category} | QP {qp} | {frame} → CD={cd:.6f}")

                if cds:
                    avg_cd = float(np.mean(cds))
                    avg_results.append({
                        "codec": codec_name,
                        "category": category,
                        "qp": qp if qp is not None else "N/A",
                        "average_chamfer_distance": avg_cd
                    })
                    print(f"[AVERAGE] {codec_name} | {category} | QP {qp} → 평균 CD={avg_cd:.6f}")

    with open(frame_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["codec", "category", "qp", "frame", "chamfer_distance"])
        writer.writeheader()
        writer.writerows(frame_results)

    with open(avg_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["codec", "category", "qp", "average_chamfer_distance"])
        writer.writeheader()
        writer.writerows(avg_results)

    print(f"\n✅ {codec_name} 결과 저장 완료 → {frame_csv}, {avg_csv}")

# -----------------------------
# 실행 예시
# -----------------------------
if __name__ == "__main__":
    gt_base = "/home/knuvi/dataset/Blind_images_v2"

    #categories = ["backpack", "ball", "book", "bottle", "chair",
     #            "cup", "handbag", "laptop", "plant", "teddybear", "vase"]
    categories = ["backpack", "ball", "book", "chair",
                      "handbag", "laptop", "plant", "teddybear", "vase"]

    # --- AVC ---
    avc_base = "/home/knuvi/vggtoutput/Blind_images_v2/avc"
    avc_pattern = "{base}/output_AVCRA{qp}/output_{category}"
    avc_qps = [42, 47]
    evaluate_codec(gt_base, avc_base, "AVC", avc_pattern, categories, avc_qps)

    # --- JPEG ---
    jpeg_base = "/home/knuvi/vggtoutput/Blind_images_v2/jpeg"
    jpeg_pattern = "{base}/output_JPEG{qp}/output_{category}"
    jpeg_qps = [20, 10]
    evaluate_codec(gt_base, jpeg_base, "JPEG", jpeg_pattern, categories, jpeg_qps)

    # --- ORIGINAL ---
  #  orig_base = "/home/knuvi/vggtoutput/Blind_images_v2/original"
  #  orig_pattern = "{base}/output_{category}"
   # evaluate_codec(gt_base, orig_base, "ORIGINAL", orig_pattern, categories, [])