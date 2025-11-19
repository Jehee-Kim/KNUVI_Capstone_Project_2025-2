# Image/Video Integrated Compression Pipeline

## Overview

This project provides a command-line interface (CLI) pipeline for automating image and video compression. It allows users to easily encode various media files using different codecs and quality settings through a single, unified command structure. The pipeline is designed to be modular, calling specialized scripts for each codec.

## Features

- **Unified Interface**: A single `main.py` script to handle all operations.
- **Multiple Codecs**: Supports **HEVC** (High Efficiency Video Coding), **AVC** (H.264), and **JPEG** (for standard images).
- **Flexible Input**: Can process a single file or all supported files within a directory.
- **Quality Control**: Easily set the desired quality level using the `--QP` argument.
- **Configurable Paths**: The path to the HEVC encoder can be specified as a command-line argument.
- **Robust Logging**: Provides clear, real-time feedback on the compression process.

## Prerequisites

Before running the pipeline, please ensure the following requirements are met:

1.  **Python 3**: The main script and JPEG encoder are written in Python 3.
2.  **FFmpeg**: Required for **AVC (H.264)** encoding. Ensure it is installed and in your system PATH.
3.  **Pillow Library**: The JPEG script requires the Pillow library. Install it via pip:
    ```bash
    pip install Pillow
    ```
4.  **Script Permissions**: The shell scripts need to be executable. Grant permissions using `chmod`:
    ```bash
    chmod +x Code/for/CompressionSW/*.sh
    ```
5.  **HEVC Encoder**: You must have an HEVC encoder executable (e.g., the HM reference software's `TAppEncoder`). You will need to provide the path to this executable for HEVC encoding.

## Usage

The main script `main.py` is the entry point for all operations.

### General Command

```bash
python3 Code/for/CompressionSW/main.py --codec <CODEC> --QP <VALUE> --input <PATH> --output <PATH> [OPTIONS]
```

### Examples

**1. HEVC Encoding**

Encodes a raw YUV video file. The `--width` and `--height` arguments are **required**.

```bash
# Encode a 1920x1080 YUV file with a QP of 27
python3 Code/for/CompressionSW/main.py \
    --codec HEVC \
    --QP 27 \
    --input /path/to/video.yuv \
    --output ./hevc_results \
    --width 1920 \
    --height 1080 \
    --encoder_path /path/to/your/TAppEncoder
```

**2. AVC (H.264) Encoding**

Encodes a video file using FFmpeg. Supports both raw YUV and standard video formats.

```bash
# Encode a video file (mp4, avi, etc.) with a QP of 30
python3 Code/for/CompressionSW/main.py \
    --codec AVC \
    --QP 30 \
    --input /path/to/video.mp4 \
    --output ./avc_results

# Encode a raw YUV file (requires width and height)
python3 Code/for/CompressionSW/main.py \
    --codec AVC \
    --QP 30 \
    --input /path/to/raw_video.yuv \
    --output ./avc_results \
    --width 1920 \
    --height 1080
```

**3. JPEG Compression**

Compresses a standard image file (e.g., PNG, BMP) into JPEG format.

```bash
# Compress an image with a quality setting of 90
python3 Code/for/CompressionSW/main.py \
    --codec JPEG \
    --QP 90 \
    --input /path/to/image.png \
    --output ./jpeg_results
```

## Argument Reference

- `--codec`: The codec to use (`HEVC`, `AVC`, or `JPEG`).
- `--QP`: The quality/quantization parameter.
  - **HEVC/AVC**: Quantization Parameter (Lower = Higher Quality).
  - **JPEG**: Quality Score (Higher = Higher Quality, 1-95).
- `--input`: Path to the source file or directory.
- `--output`: Path to the destination directory for results.
- `--width`: Frame width for the input video. **Required for HEVC and raw YUV inputs in AVC.**
- `--height`: Frame height for the input video. **Required for HEVC and raw YUV inputs in AVC.**
- `--encoder_path`: (Optional) Path to the HEVC encoder executable.

## Scripts Overview

- `main.py`: The main controller. It parses user arguments and calls the appropriate script.
- `encode_hevc_single.sh`: Encodes a single YUV file using an HEVC encoder (HM).
- `encode_avc_single.sh`: Encodes a single file using FFmpeg (H.264).
- `encode_jpeg_single.py`: Compresses a single image file into JPEG format using Pillow.