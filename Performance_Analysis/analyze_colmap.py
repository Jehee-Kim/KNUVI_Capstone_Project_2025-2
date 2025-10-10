#!/usr/bin/env python3
# analyze_colmap.py
import sys
import os
from collections import defaultdict
import numpy as np

def parse_points3D(path):
    pts = {}
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('#') or len(line.strip()) == 0:
                continue
            parts = line.strip().split()
            if len(parts) < 10:  # 너무 짧으면 skip
                continue
            pid = int(parts[0])
            x, y, z = map(float, parts[1:4])
            error = float(parts[7])
            track_length = int(parts[8])
            # track 정보는 optional, 안 쓰면 빈 리스트
            track = []
            if len(parts) > 9:
                for i in range(track_length):
                    try:
                        img_id = int(parts[9 + 2*i])
                        pt2d_idx = int(parts[9 + 2*i + 1])
                        track.append((img_id, pt2d_idx))
                    except:
                        continue
            pts[pid] = {'xyz': (x,y,z), 'err': error, 'track_len': track_length, 'track': track}
    return pts

def parse_images(path):
    imgs = {}
    with open(path, 'r') as f:
        lines = [l.strip() for l in f if not l.startswith('#') and len(l.strip()) > 0]
        i = 0
        while i < len(lines):
            parts = lines[i].split()
            if len(parts) < 10:
                i += 1
                continue
            try:
                img_id = int(parts[0])
            except:
                i += 1
                continue
            name = parts[9]
            imgs[img_id] = {'name': name}
            i += 2  # 두 줄씩 건너뛰기 (두 번째 줄은 POINTS2D)
    return imgs

def analyze(sparse_dir):
    pts = parse_points3D(os.path.join(sparse_dir,'points3D.txt'))
    imgs = parse_images(os.path.join(sparse_dir,'images.txt'))
    # stats
    errs = []
    track_lengths = []
    observations_per_image = defaultdict(int)
    image_error_acc = defaultdict(float)
    image_error_count = defaultdict(int)

    for pid, info in pts.items():
        errs.append(info['err'])
        track_lengths.append(info['track_len'])
        for (img_id, _) in info['track']:
            observations_per_image[img_id] += 1
            image_error_acc[img_id] += info['err']
            image_error_count[img_id] += 1

    # convert to arrays
    errs = np.array(errs)
    track_lengths = np.array(track_lengths)
    obs_counts = np.array(list(observations_per_image.values()))
    # per-image mean error (approx)
    img_mean_err = {img_id: image_error_acc[img_id]/image_error_count[img_id] for img_id in image_error_acc}

    # print summary
    print("=== SUMMARY for", sparse_dir)
    print("num_points:", len(pts))
    print("num_images (in images.txt):", len(imgs))
    print("registered images (images that appear in tracks):", len(observations_per_image))
    print("total observations (sum per-image):", sum(observations_per_image.values()))
    print("mean track length:", np.mean(track_lengths))
    print("median track length:", np.median(track_lengths))
    print("track length percentiles (10,50,90):", np.percentile(track_lengths,[10,50,90]))
    print("mean reprojection error (points):", np.mean(errs))
    print("median reprojection error (points):", np.median(errs))
    print("reproj error percentiles (10,50,90):", np.percentile(errs,[10,50,90]))
    print("mean observations per image:", np.mean(obs_counts))
    print("median observations per image:", np.median(obs_counts))
    # worst points
    worst_pts_idx = np.argsort(-errs)[:10]
    print("\nTop 10 worst points (id, err, track_len):")
    pts_items = list(pts.items())
    for idx in worst_pts_idx:
        pid, info = pts_items[idx]
        print(pid, info['err'], info['track_len'], "-> observed in images:", [t[0] for t in info['track']])
    # worst images by approx mean error
    sorted_imgs = sorted(img_mean_err.items(), key=lambda x:-x[1])[:10]
    print("\nTop 10 images by approx mean assigned reproj error (img_id, mean_err, obs_count):")
    for img_id, mean_err in sorted_imgs:
        print(img_id, round(mean_err,3), observations_per_image[img_id], imgs.get(img_id,{}).get('name','-'))
    # return dict for programmatic use
    return {
        'num_points': len(pts),
        'num_images': len(imgs),
        'registered_images': len(observations_per_image),
        'total_observations': sum(observations_per_image.values()),
        'mean_track_length': float(np.mean(track_lengths)),
        'mean_reproj_error': float(np.mean(errs)),
        'obs_counts': observations_per_image,
        'img_mean_err': img_mean_err
    }

if __name__=='__main__':
    if len(sys.argv)!=2:
        print("Usage: python analyze_colmap.py /path/to/sparse/0")
        sys.exit(1)
    analyze(sys.argv[1])


#python3 analyze_colmap.py /mnt/c/Users/PC012/Desktop/BCE/HEVC_37/datasets/1_bicycle/sparse/0 > qp37_analysis.txt
