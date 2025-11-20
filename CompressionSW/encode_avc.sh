#!/bin/bash

###############################################################
#  AVCRA Pipeline Shell Script
#  - Creates compressed video using FFmpeg (QP-based)
#  - Extracts PNG frames
#  - Renames frames to {original}_AVCRA_{QP}.png
###############################################################

# --- Usage Example ---
# ./run_avcra.sh \
#   --input /Users/jehee/Documents/KNU/intern/Blind_images_v2 \
#   --output /Users/jehee/Documents/KNU/intern/Blind_images_v2/avc \
#   --qp 27
#
###############################################################

# Default values
QP=""
INPUT_DIR=""
OUTPUT_DIR=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --qp) QP="$2"; shift ;;
        --input) INPUT_DIR="$2"; shift ;;
        --output) OUTPUT_DIR="$2"; shift ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
    shift
done

if [[ -z "$QP" || -z "$INPUT_DIR" || -z "$OUTPUT_DIR" ]]; then
    echo "Usage: ./run_avcra.sh --qp [QP] --input [INPUT_DIR] --output [OUTPUT_DIR]"
    exit 1
fi

CATEGORY_LIST=("backpack" "ball" "book" "bottle" "chair" "cup" "handbag" "labtop" "plant" "teddybear" "vase")

echo "-------------------------------------------"
echo " AVCRA Pipeline Start"
echo " QP = $QP"
echo " Input  = $INPUT_DIR"
echo " Output = $OUTPUT_DIR"
echo "-------------------------------------------"

for category in "${CATEGORY_LIST[@]}"; do
    category_path="$INPUT_DIR/$category"
    if [[ ! -d "$category_path" ]]; then
        continue
    fi

    for subfolder in "$category_path"/*; do
        subfolder_name=$(basename "$subfolder")

        # Match pattern: number_number_number
        if [[ ! "$subfolder_name" =~ ^[0-9]+_[0-9]+_[0-9]+$ ]]; then
            continue
        fi

        image_dir="$subfolder/images"
        if [[ ! -d "$image_dir" ]]; then
            continue
        fi

        # List jpg files
        files=( $(ls "$image_dir"/*.jpg 2>/dev/null) )
        if [[ ${#files[@]} -eq 0 ]]; then
            continue
        fi

        temp_video="$OUTPUT_DIR/$category/${subfolder_name}_qp${QP}.mp4"
        mkdir -p "$(dirname "$temp_video")"

        output_frames_dir="$OUTPUT_DIR/$category/$subfolder_name/images_qp${QP}"
        mkdir -p "$output_frames_dir"

        echo "▶️ Processing: $category / $subfolder_name (QP=$QP)"

        # ------------------------------
        # 1. Create compressed video
        # ------------------------------
        ffmpeg -y \
            -framerate 30 \
            -i "$image_dir/frame%06d.jpg" \
            -vf "pad=ceil(iw/2)*2:ceil(ih/2)*2" \
            -c:v libx264 \
            -profile:v high \
            -preset slow \
            -qp $QP \
            -x264-params bframes=2:keyint=48:scenecut=0 \
            -pix_fmt yuv420p \
            "$temp_video"

        # ------------------------------
        # 2. Extract PNG frames
        # ------------------------------
        ffmpeg -y \
            -i "$temp_video" \
            "$output_frames_dir/frame_%06d.png"

        # ------------------------------
        # 3. Rename frames
        # ------------------------------
        idx=1
        for img_file in "${files[@]}"; do
            orig_stem=$(basename "$img_file" .jpg)
            src="$output_frames_dir/frame_$(printf "%06d" "$idx").png"
            dst="$output_frames_dir/${orig_stem}_AVCRA_${QP}.png"

            if [[ -f "$src" ]]; then
                mv "$src" "$dst"
            fi

            idx=$((idx + 1))
        done

        echo "✅ Completed: $category / $subfolder_name  →  $output_frames_dir"
    done

done

echo "-------------------------------------------"
echo " AVCRA Pipeline Finished!"
echo "-------------------------------------------"
