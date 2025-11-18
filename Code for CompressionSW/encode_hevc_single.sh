#!/bin/bash

# Default values
QP=""
INPUT_FILE=""
OUTPUT_FILE=""
WIDTH=""
HEIGHT=""
# NOTE: TAppEncoder also requires the number of frames. Hardcoding to 300 for now.
FRAMES="300" 
# NOTE: The config file path is hardcoded.
CFG_PATH="/root/HM/cfg/encoder_randomaccess_main.cfg"
# Default encoder path. Can be overridden with the --encoder_path argument.
ENCODER_PATH="/root/HM/bin/umake/gcc-11.4/x86_64/release/TAppEncoder"

# Parse named arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --qp) QP="$2"; shift ;;
        --input) INPUT_FILE="$2"; shift ;;
        --output) OUTPUT_FILE="$2"; shift ;;
        --width) WIDTH="$2"; shift ;;
        --height) HEIGHT="$2"; shift ;;
        --encoder_path) ENCODER_PATH="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Check for required arguments
if [[ -z "$QP" || -z "$INPUT_FILE" || -z "$OUTPUT_FILE" || -z "$WIDTH" || -z "$HEIGHT" ]]; then
    echo "Usage: $0 --qp <value> --input <file> --output <file> --width <value> --height <value>"
    echo "Optional: --encoder_path <path>"
    exit 1
fi

# Create output directories
RECON_DIR=$(dirname "$OUTPUT_FILE")
# Following the original script's structure, create a parallel 'bitstream' directory
BITSTREAM_DIR="$(dirname "$RECON_DIR")/bitstream"
mkdir -p "$RECON_DIR"
mkdir -p "$BITSTREAM_DIR"

# Define output file paths
RECON_FILE="$OUTPUT_FILE"
BASENAME=$(basename "$OUTPUT_FILE" .yuv)
BITSTREAM_FILE="$BITSTREAM_DIR/${BASENAME}.bin"

echo "--- Starting HEVC Encoding ---"
echo "Input: $INPUT_FILE"
echo "Output (Recon): $RECON_FILE"
echo "Output (Bitstream): $BITSTREAM_FILE"
echo "QP: $QP"
echo "Resolution: ${WIDTH}x${HEIGHT}"
echo "Encoder Path: $ENCODER_PATH"
echo "----------------------------"

# Check if the encoder file actually exists
if [ ! -f "$ENCODER_PATH" ]; then
    echo "Error: HEVC Encoder not found at: $ENCODER_PATH"
    echo "Please specify the correct path using the --encoder_path argument."
    exit 1
fi

# Execute the HM Encoder
"$ENCODER_PATH" \
    -c "$CFG_PATH" \
    -i "$INPUT_FILE" \
    -o "$RECON_FILE" \
    -wdt "$WIDTH" \
    -hgt "$HEIGHT" \
    -b "$BITSTREAM_FILE" \
    -q "$QP" \
    -fr 30 \
    -f "$FRAMES" # Using hardcoded frame count

ret=$?
if [ $ret -eq 0 ]; then
    echo "Encoding finished successfully."
else
    echo "Error: Encoding failed with exit code $ret."
fi

exit $ret