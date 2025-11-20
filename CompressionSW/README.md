# Image/Video Integrated Compression Pipeline

## Overview

This project provides a command-line interface (CLI) pipeline for automating image and video compression. It allows users to easily encode various media files using different codecs and quality settings through a single, unified command structure. The pipeline is designed to be modular, calling specialized scripts for each codec.

## Features

- **Unified Interface**: A single `main.py` script to handle all operations.
- **Multiple Codecs**: Supports **HEVC** (High Efficiency Video Coding), **AVC** (H.264), and **JPEG** (for standard images).
- **Flexible Input**: Can process a single file or all supported files within a directory.
  - **Video**: `.mp4`, `.avi`, `.mov`, `.mkv`, `.yuv`
  - **Image**: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`
- **Quality Control**: Easily set the desired quality level using the `--QP` argument.
- **Speed Control**: Adjust encoding speed using the `--preset` argument (e.g., `ultrafast`, `medium`, `veryslow`).
- **Robust Logging**: Provides clear, real-time feedback on the compression process.

## Prerequisites

Before running the pipeline, please ensure the following requirements are met:

1.  **Python 3**: The main script and JPEG encoder are written in Python 3.
2.  **FFmpeg**: Required for **AVC (H.264)** and **HEVC** encoding. Ensure it is installed and in your system PATH.
3.  **Pillow Library**: The JPEG script requires the Pillow library. Install it via pip:
    ```bash
    pip install Pillow
    ```
4.  **Script Permissions**: The shell scripts need to be executable. Grant permissions using `chmod`:
    ```bash
    chmod +x *.sh
    ```

## Usage

The main script `main.py` is the entry point for all operations.
**Note**: All commands assume you are in the directory containing `main.py`.

### General Command

```bash
python3 main.py --codec <CODEC> --QP <VALUE> --input <PATH> --output <PATH> [OPTIONS]
```

### Examples

**1. HEVC Encoding**

Fast encoding using FFmpeg. Produces `.mp4` files.

```bash
# Encode a video file with a QP of 27 and 'fast' preset
python3 main.py \
    --codec HEVC \
    --QP 27 \
    --input /path/to/video.mp4 \
    --output ./hevc_results \
    --preset fast
```

**2. AVC (H.264) Encoding**

Encodes a video file using FFmpeg.

```bash
# Encode a video file with a QP of 30 and 'ultrafast' preset
python3 main.py \
    --codec AVC \
    --QP 30 \
    --input /path/to/video.mp4 \
    --output ./avc_results \
    --preset ultrafast
```

**3. JPEG Compression**

Compresses a standard image file (e.g., PNG, BMP) into JPEG format.

```bash
# Compress an image with a quality setting of 90
python3 main.py \
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
- `--preset`: Encoding speed preset (default: `medium`). Choices: `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`.
- `--width`: Frame width. **Required for raw YUV inputs.**
- `--height`: Frame height. **Required for raw YUV inputs.**

## Scripts Overview

- `main.py`: The main controller. It parses user arguments and calls the appropriate script.
- `encode_hevc_single.sh`: Handles HEVC encoding using FFmpeg.
- `encode_avc_single.sh`: Handles AVC (H.264) encoding using FFmpeg.
- `encode_jpeg_single.py`: Compresses a single image file into JPEG format using Pillow.