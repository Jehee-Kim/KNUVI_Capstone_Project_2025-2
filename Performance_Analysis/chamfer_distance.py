import numpy as np
import trimesh
from scipy.spatial import cKDTree
import os
import glob
import pandas as pd
import argparse

def calculate_chamfer_distance(point_cloud_A, point_cloud_B):
    """
    Calculate Chamfer distance between two point clouds A and B.
    """
    kdtree_A = cKDTree(point_cloud_A)
    kdtree_B = cKDTree(point_cloud_B)

    # Calculate sum of squared distances from A to B
    distances_A_to_B_sq, _ = kdtree_B.query(point_cloud_A)
    chamfer_A_to_B = np.sum(distances_A_to_B_sq**2)

    # Calculate sum of squared distances from B to A
    distances_B_to_A_sq, _ = kdtree_A.query(point_cloud_B)
    chamfer_B_to_A = np.sum(distances_B_to_A_sq**2)

    # Calculate Chamfer distance (average of squared distances)
    chamfer_distance = (chamfer_A_to_B / len(point_cloud_A) + chamfer_B_to_A / len(point_cloud_B))
    return chamfer_distance

def load_ply_points(ply_path):
    """
    Load point cloud data from PLY file.
    """
    try:
        mesh = trimesh.load(ply_path)
        if isinstance(mesh, trimesh.Trimesh):
            vertices = mesh.vertices
        elif isinstance(mesh, trimesh.PointCloud):
            vertices = mesh.vertices
        else:
            print(f"Warning: {ply_path} has unexpected format.")
            return None
        
        # Check for empty point cloud
        if vertices is None or len(vertices) == 0:
            print(f"Warning: {ply_path} is empty point cloud (vertex count: 0)")
            return None
            
        return vertices
        
    except Exception as e:
        print(f"Error loading file: {ply_path} - {e}")
        return None

def parse_source_txt(source_txt_path):
    """
    Parse source.txt file and return list of (category, gt_ply_path, pred_parent_dir) tuples.

    Expected format:
      gt1
      /abs/path/to/.../pointcloud.ply
      ...
      pred1
      /abs/path/to/output_category
      ...

    gtN and predN with matching numbers are considered as pairs.
    Category name is determined by the following priority:
      1) Remove 'output_' prefix from pred directory base name
      2) Extract category from gt path (Blind_images_v2/<category>/...)
      3) Use pred directory base name
    """
    if not os.path.isfile(source_txt_path):
        raise FileNotFoundError(f"source file not found: {source_txt_path}")

    with open(source_txt_path, 'r') as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    gt_map = {}
    pred_map = {}

    expect_key = None
    for token in lines:
        lower = token.lower()
        if lower.startswith('gt') or lower.startswith('pred'):
            expect_key = lower
            continue
        # token is a path line
        if expect_key is None:
            raise ValueError('Invalid source.txt format: key expected before path')
        if expect_key.startswith('gt'):
            idx = expect_key[2:]
            gt_map[idx] = token
        elif expect_key.startswith('pred'):
            idx = expect_key[4:]
            pred_map[idx] = token
        expect_key = None

    pairs = []
    all_indices = sorted(set(gt_map.keys()) & set(pred_map.keys()), key=lambda x: int(x))
    if not all_indices:
        raise ValueError('No matching gtN/predN pairs found in source file')

    for idx in all_indices:
        gt_path = gt_map[idx]
        pred_dir = pred_map[idx]
        if not os.path.isfile(gt_path):
            raise FileNotFoundError(f"GT ply does not exist: {gt_path}")
        if not os.path.isdir(pred_dir):
            raise NotADirectoryError(f"Pred directory does not exist: {pred_dir}")

        # Derive category name
        pred_base = os.path.basename(pred_dir.rstrip(os.sep))
        category = pred_base
        if pred_base.startswith('output_') and len(pred_base) > len('output_'):
            category = pred_base[len('output_'):]
        else:
            # try to read category from gt path
            parts = gt_path.split(os.sep)
            if 'Blind_images_v2' in parts:
                i = parts.index('Blind_images_v2')
                if i + 1 < len(parts):
                    category = parts[i + 1]

        pairs.append((category, gt_path, pred_dir))

    return pairs

def process_pair(category, gt_ply_path, parents_directory, output_dir):
    """Process single category pair and generate <category>_CD.csv file."""
    output_csv_filename = os.path.join(output_dir, f"{category}_CD.csv")
    error_csv_filename = os.path.join(output_dir, f"{category}_error.csv")

    # Check existing result files and load already processed frames
    existing_results = {}
    existing_errors = {}
    
    if os.path.exists(output_csv_filename):
        try:
            df_existing = pd.read_csv(output_csv_filename)
            existing_results = dict(zip(df_existing['directory_name'], df_existing['score']))
            print(f"Found {len(existing_results)} frames in existing result file.")
        except Exception as e:
            print(f"Failed to read existing result file: {e}")
    
    if os.path.exists(error_csv_filename):
        try:
            df_errors = pd.read_csv(error_csv_filename)
            existing_errors = dict(zip(df_errors['frame_number'], df_errors['error_message']))
            print(f"Found {len(existing_errors)} frames in existing error file.")
        except Exception as e:
            print(f"Failed to read existing error file: {e}")

    # 1. Load GT point cloud file
    print(f"Loading GT point cloud file: {gt_ply_path}")
    gt_points = load_ply_points(gt_ply_path)

    if gt_points is None:
        print("Failed to load GT point cloud, skipping this pair.")
        return

    print(f"GT point cloud loaded successfully. Point count: {len(gt_points)}")
    print("-" * 50)

    # 2. Find all 'points.ply' files under parent directory
    ply_files_to_compare = glob.glob(os.path.join(parents_directory, '**', 'points.ply'), recursive=True)

    if not ply_files_to_compare:
        print(f"Warning: No 'points.ply' files found under '{parents_directory}' directory.")
        return

    # 3. Initialize result storage lists
    results = []
    errors = []
    skipped_count = 0

    # 4. Iterate through each file and calculate Chamfer distance
    for file_path in ply_files_to_compare:
        # Extract target directory name
        directory_name = os.path.basename(os.path.dirname(file_path))
        
        # Skip only frames with successful results (retry errors)
        if directory_name in existing_results:
            print(f"⏭️  {directory_name} already processed successfully (existing result: {existing_results[directory_name]:.6f})")
            skipped_count += 1
            continue
        
        # Retry frames that had errors
        if directory_name in existing_errors:
            print(f"🔄 {directory_name} had previous error, retrying (previous error: {existing_errors[directory_name]})")
        
        print(f"Loading target file: {file_path}")
        
        try:
            output_points = load_ply_points(file_path)

            if output_points is None:
                error_msg = "Point cloud load failed or empty point cloud"
                print(f"Target point cloud load failed or empty. Moving to next file.")
                errors.append({
                    'frame_number': directory_name,
                    'error_message': error_msg,
                    'file_path': file_path
                })
                continue

            # Calculate Chamfer distance
            cd = calculate_chamfer_distance(gt_points, output_points)
        
            # Add result to list
            results.append({
                'directory_name': directory_name,
                'score': cd
            })
        
            # Print real-time results to show progress
            print(f"-> {directory_name} Chamfer Distance: {cd:.6f}")
            print("-" * 50)
            
        except Exception as e:
            error_msg = f"Error during calculation: {str(e)}"
            print(f"Error occurred: {directory_name} - {error_msg}")
            errors.append({
                'frame_number': directory_name,
                'error_message': error_msg,
                'file_path': file_path
            })

    # 5. Convert results to DataFrame and save to CSV file
    if results:
        # Combine existing and new results
        all_results = []
        
        # Add existing results
        for dir_name, score in existing_results.items():
            all_results.append({'directory_name': dir_name, 'score': score})
        
        # Add new results
        for result in results:
            all_results.append(result)
        
        df_results = pd.DataFrame(all_results)
        # Sort by directory name in ascending order
        df_results = df_results.sort_values('directory_name', ascending=True)
        df_results.to_csv(output_csv_filename, index=False)
        print(f"✅ {category} Chamfer distance calculation completed and saved to '{output_csv_filename}'.")
    elif existing_results:
        # No new results but existing results available
        print(f"✅ {category} No new frames processed, maintaining existing results.")
    else:
        print("No data to calculate, CSV file not created.")
    
    # 6. Create error CSV file if errors occurred
    if errors:
        # Combine existing and new errors (exclude existing errors, add only new ones)
        all_errors = []
        
        # Keep only existing errors that were not newly processed
        for frame_num, error_msg in existing_errors.items():
            # Keep only if not newly processed
            if not any(e['frame_number'] == frame_num for e in results):
                all_errors.append({'frame_number': frame_num, 'error_message': error_msg, 'file_path': ''})
        
        # Add new errors
        for error in errors:
            all_errors.append(error)
        
        df_errors = pd.DataFrame(all_errors)
        df_errors.to_csv(error_csv_filename, index=False)
        print(f"⚠️  {len(errors)} new errors occurred and saved to '{error_csv_filename}'.")
    elif existing_errors:
        print(f"✅ {category} No new error frames, maintaining existing error information.")
    else:
        print(f"✅ {category} No errors occurred during processing.")
    
    # 7. Print processing summary
    total_processed = len(existing_results) + len(existing_errors) + len(results) + len(errors)
    print(f"📊 {category} processing summary:")
    print(f"   - Existing results: {len(existing_results)}")
    print(f"   - Existing errors: {len(existing_errors)}")
    print(f"   - New results: {len(results)}")
    print(f"   - New errors: {len(errors)}")
    print(f"   - Skipped frames: {skipped_count}")
    print(f"   - Total processed frames: {total_processed}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source_txt', type=str, required=True, help='Path to source.txt defining gtN/predN pairs')
    parser.add_argument('--output_dir', type=str, default='.', help='Directory to save CSV files for each pair')
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    pairs = parse_source_txt(args.source_txt)
    print(f"Processing {len(pairs)} pairs in total.")
    for category, gt_ply_path, pred_parent_dir in pairs:
        print("=" * 60)
        print(f"Category: {category}")
        print(f"GT: {gt_ply_path}")
        print(f"PRED parent directory: {pred_parent_dir}")
        print("=" * 60)
        process_pair(category, gt_ply_path, pred_parent_dir, args.output_dir)