# Image/Video Integrated Compression Pipeline

## Overview

This project provides a command-line interface (CLI) pipeline for automating image and video compression. It allows users to easily encode various media files using different codecs and quality settings through a single, unified command structure. The pipeline is designed to be modular, calling specialized scripts for each codec.

## Features

- **Unified Interface**: A single `main.py` script to handle all operations.
- **Multiple Codecs**: Supports HEVC (for YUV raw video) and JPEG (for standard images).
- **Flexible Input**: Can process a single file or all supported files within a directory.
- **Quality Control**: Easily set the desired quality level using the `--QP` argument.
- **Configurable Paths**: The path to the HEVC encoder can be specified as a command-line argument, avoiding hardcoded paths.
- **Robust Logging**: Provides clear, real-time feedback on the compression process.

## Prerequisites

Before running the pipeline, please ensure the following requirements are met:

1.  **Python 3**: The main script and JPEG encoder are written in Python 3.
2.  **Pillow Library**: The JPEG script requires the Pillow library. Install it via pip:
    ```bash
    pip install Pillow
    ```
3.  **Script Permissions**: The HEVC encoder script needs to be executable. Grant permissions using `chmod`:
    ```bash
    chmod +x "Code for CompressionSW/encode_hevc_single.sh"
    ```
4.  **HEVC Encoder**: You must have an HEVC encoder executable (e.g., the HM reference software's `TAppEncoder`). You will need to provide the path to this executable.

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

**2. JPEG Compression**

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

- `--codec`: The codec to use (`HEVC` or `JPEG`).
- `--QP`: The quality/quantization parameter. **Note the different meanings per codec (see below).**
- `--input`: Path to the source file or directory.
- `--output`: Path to the destination directory for results.
- `--width`: Frame width for the input video. **Required for HEVC.**
- `--height`: Frame height for the input video. **Required for HEVC.**
- `--encoder_path`: (Optional) Path to the HEVC encoder executable. If not provided, the script uses a default path.

## Important Notes

- **Meaning of `--QP`**:
  - For **HEVC**, `--QP` is the Quantization Parameter. A **lower** value means **higher** quality.
  - For **JPEG**, `--QP` is the Quality Score. A **higher** value means **higher** quality (1-95 recommended).

- **HEVC Input Format**: The HEVC script is designed **only for raw YUV video files**. It will not work with standard formats like MP4 or MOV.

- **HEVC Script Configuration**: The `encode_hevc_single.sh` script still contains some hardcoded values that you may need to be aware of:
  - `CFG_PATH`: The path to the encoder configuration file (`.cfg`).
  - `FRAMES`: The number of frames to encode is hardcoded to `300`.

## Scripts Overview

- `main.py`: The main controller. It parses user arguments and calls the appropriate script.
- `encode_hevc_single.sh`: A shell script that takes arguments to encode a single YUV file using an HEVC encoder.
- `encode_jpeg_single.py`: A Python script that takes arguments to compress a single image file into JPEG format using the Pillow library.