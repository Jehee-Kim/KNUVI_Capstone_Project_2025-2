#!/bin/bash

# Default values
QP=""
INPUT_FILE=""
OUTPUT_FILE=""
WIDTH=""
HEIGHT=""
PRESET="medium"
ALL_INTRA=false

# Parse named arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --qp) QP="$2"; shift ;;
        --input) INPUT_FILE="$2"; shift ;;
        --output) OUTPUT_FILE="$2"; shift ;;
        --width) WIDTH="$2"; shift ;;
        --height) HEIGHT="$2"; shift ;;
        --preset) PRESET="$2"; shift ;;
        --all_intra) ALL_INTRA=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check for required arguments
if [[ -z "$QP" || -z "$INPUT_FILE" || -z "$OUTPUT_FILE" ]]; then
    echo "Usage: $0 --qp <value> --input <file> --output <file> [--width <value> --height <value>] [--preset <value>]"
    exit 1
fi

echo "--- Starting HEVC Encoding ---"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "QP: $QP"

# ==========================================
# Mode: Use FFmpeg (libx265)
# ==========================================
echo "Mode: FFmpeg (libx265)"

CMD="ffmpeg -y"

# Handle YUV raw input
if [[ "$INPUT_FILE" == *.yuv ]]; then
    if [[ -z "$WIDTH" || -z "$HEIGHT" ]]; then
        echo "Error: Raw YUV input requires --width and --height."
        exit 1
    fi
    CMD="$CMD -f rawvideo -vcodec rawvideo -s ${WIDTH}x${HEIGHT} -pix_fmt yuv420p -framerate 30"
fi

CMD="$CMD -i \"$INPUT_FILE\""

# Ensure dimensions are even
CMD="$CMD -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\""

# HEVC Encoding settings
# x265-params: qp=X sets the quantization parameter.
if [ "$ALL_INTRA" = true ]; then
    # All-Intra: Keyint=1 (Every frame is an I-frame), No B-frames usually implied or explicit
    CMD="$CMD -c:v libx265 -preset $PRESET -x265-params qp=$QP:keyint=1"
else
    # Default (Random Access): Keyint=48, B-frames=2 (Default behavior or explicit)
    CMD="$CMD -c:v libx265 -preset $PRESET -x265-params qp=$QP:keyint=48:bframes=2"
fi

CMD="$CMD -pix_fmt yuv420p"
CMD="$CMD \"$OUTPUT_FILE\""

echo "Command: $CMD"
eval $CMD

ret=$?
if [ $ret -eq 0 ]; then
    echo "HEVC Encoding finished successfully."
else
    echo "Error: HEVC Encoding failed with exit code $ret."
fi

exit $ret