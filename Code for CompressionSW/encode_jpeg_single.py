import argparse
from PIL import Image
import os
import sys

def compress_jpeg(input_path, output_path, quality):
    """
    Compresses an image to JPEG format with a given quality.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with Image.open(input_path) as img:
            # Convert image to RGB mode for saving as JPEG
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_path)
            os.makedirs(output_dir, exist_ok=True)

            # Save the image as JPEG
            img.save(output_path, "JPEG", quality=quality, optimize=True)
            print(f"Success: Saved {output_path} with quality={quality}")

    except Exception as e:
        print(f"Error: Failed to process {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Single-file JPEG compressor.")
    parser.add_argument("--input", required=True, help="Path to the input image.")
    parser.add_argument("--output", required=True, help="Path for the output JPEG image.")
    # In JPEG, quality is a value from 1-95.
    parser.add_argument("--quality", required=True, type=int, help="JPEG quality (1-95 recommended).")
    
    args = parser.parse_args()

    if not 1 <= args.quality <= 95:
        print(f"Warning: Quality value {args.quality} is outside the recommended range (1-95).", file=sys.stderr)

    compress_jpeg(args.input, args.output, args.quality)

if __name__ == "__main__":
    main()