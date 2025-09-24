import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os

def visualize_chamfer_distance(file_path):
    """
    Read Chamfer distance data from the given CSV file path and generate 4 scatter plots.
    - First: Frame number vs score
    - Remaining 3: Frame_codec_QP vs score sorted by Chamfer distance score in ascending order (by codec)
    """
    try:
        if not os.path.exists(file_path):
            print(f"Error: The specified file does not exist -> '{file_path}'")
            return

        df = pd.read_csv(file_path)
        
        if 'directory_name' not in df.columns or 'score' not in df.columns:
            print(f"Error: Required columns ('directory_name', 'score') are missing in '{os.path.basename(file_path)}'.")
            return

        print(f"\n--- Processing '{os.path.basename(file_path)}' ---")
        
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{os.path.basename(file_path)}' is empty.")
        return
    except Exception as e:
        print(f"An error occurred while reading '{os.path.basename(file_path)}': {e}")
        return

    # Create 'frame_number', 'codec', 'simple_label' columns
    df['frame_number'] = df['directory_name'].apply(lambda x: int(x.split('_')[0].replace('frame', '')))
    df['codec'] = df['directory_name'].apply(lambda x: x.split('_')[1])
    # New label format: frame_number_codec_QP
    # Modified to use only the last 3 digits of frame number
    df['simple_label'] = df['directory_name'].apply(lambda x: f"{x.split('_')[0].replace('frame', '')[-3:]}_{'_'.join(x.split('_')[1:])}")
    
    # Generate image filenames
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    frame_scatter_filename = f"{base_name}_frame_scatter.png"
    
    # Matplotlib font settings for English output
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['axes.unicode_minus'] = False

    # 1. Scatter Plot (Overall Frame vs. Chamfer Distance)
    df_sorted_by_frame = df.sort_values(by='frame_number')
    plt.figure(figsize=(12, 6))
    plt.scatter(df_sorted_by_frame['frame_number'], df_sorted_by_frame['score'], alpha=0.7)
    plt.title(f'[{base_name}] Chamfer Distance vs. Frame Number (All Codecs)')
    plt.xlabel('Frame Number')
    plt.ylabel('Chamfer Distance Score')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(frame_scatter_filename)
    plt.close()
    
    # 2-4. Scatter Plots for each codec (sorted by score)
    codecs = df['codec'].unique()
    for codec in codecs:
        df_codec = df[df['codec'] == codec].copy()
        df_sorted_codec = df_codec.sort_values(by='score', ascending=True)
        
        plt.figure(figsize=(20, 8))
        
        plt.scatter(df_sorted_codec['simple_label'], df_sorted_codec['score'], alpha=0.7)
        plt.title(f'[{base_name}] Chamfer Distance vs. {codec} (Sorted by Score)')
        plt.xlabel('Frame_Codec_QP')
        plt.ylabel('Chamfer Distance Score')
        plt.xticks(rotation=90, fontsize=8)
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"{base_name}_{codec}_sorted_scatter.png")
        plt.close()

    print(f"Visualization complete. 1 overall plot and {len(codecs)} codec-specific plots have been created.")


def process_multiple_files(source_file='source.txt'):
    """
    Read CSV paths from 'source.txt' and visualize each file.
    """
    try:
        with open(source_file, 'r', encoding='utf-8') as f:
            file_paths = [line.strip() for line in f if line.strip()]
            
        if not file_paths:
            print("Error: The file 'source.txt' is empty or contains no valid paths.")
            return

        print(f"Read {len(file_paths)} CSV paths from '{source_file}'.")
        for path in file_paths:
            visualize_chamfer_distance(path)

    except FileNotFoundError:
        print(f"Error: The file '{source_file}' does not exist. Please create the file and add the paths.")
    except Exception as e:
        print(f"An unknown error occurred while reading the file: {e}")


# --- Code execution section ---
'''
This script will process all CSV paths listed in 'source.txt.'
ex)
    backpack_CD.csv
    ball_CD.csv
    book_CD.csv
    bottle_CD.csv   
'''
process_multiple_files()