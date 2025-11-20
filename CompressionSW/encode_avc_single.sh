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
    echo "Usage: $0 --qp <value> --input <file> --output <file> [--width <value> --height <value>]"
    exit 1
fi

# Prepare FFmpeg command
CMD="ffmpeg -y"

# Handle YUV raw input
if [[ "$INPUT_FILE" == *.yuv ]]; then
    if [[ -z "$WIDTH" || -z "$HEIGHT" ]]; then
        echo "Error: Raw YUV input requires --width and --height arguments."
        exit 1
    fi
    # Assuming YUV420P and 30fps for raw input, adjust if necessary
    CMD="$CMD -f rawvideo -vcodec rawvideo -s ${WIDTH}x${HEIGHT} -pix_fmt yuv420p -framerate 30"
fi

CMD="$CMD -i \"$INPUT_FILE\""

# Ensure dimensions are even (required for 4:2:0)
CMD="$CMD -vf \"pad=ceil(iw/2)*2:ceil(ih/2)*2\""

# Encoding settings
if [ "$ALL_INTRA" = true ]; then
    # All-Intra: Keyint=1 (Every frame is an I-frame)
    CMD="$CMD -c:v libx264 -profile:v high -preset $PRESET -qp $QP"
    CMD="$CMD -x264-params keyint=1:scenecut=0"
else
    # Default (Random Access): Keyint=48, B-frames=2
    CMD="$CMD -c:v libx264 -profile:v high -preset $PRESET -qp $QP"
    CMD="$CMD -x264-params bframes=2:keyint=48:scenecut=0"
fi
CMD="$CMD -pix_fmt yuv420p"
CMD="$CMD \"$OUTPUT_FILE\""

echo "--- Starting AVC Encoding ---"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "QP: $QP"
if [[ -n "$WIDTH" ]]; then echo "Resolution: ${WIDTH}x${HEIGHT}"; fi
echo "Command: $CMD"
echo "-----------------------------"

# Execute
eval $CMD

ret=$?
if [ $ret -eq 0 ]; then
    echo "AVC Encoding finished successfully."
else
    echo "Error: AVC Encoding failed with exit code $ret."
fi

exit $ret
