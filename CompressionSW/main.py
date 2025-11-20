import argparse
import os
import subprocess
import logging

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_command(command):
    """Runs a shell command and logs the result."""
    logging.info(f"Executing command: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, encoding='utf-8'
        )
        logging.info("STDOUT:\n" + result.stdout)
        if result.stderr:
            logging.warning("STDERR:\n" + result.stderr)
        logging.info("Command executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: Command failed to execute: {' '.join(command)}")
        logging.error(f"Return Code: {e.returncode}")
        logging.error("STDOUT:\n" + e.stdout)
        logging.error("STDERR:\n" + e.stderr)
        return False
    except FileNotFoundError:
        logging.error(f"Error: Command '{command[0]}' not found.")
        logging.error("Please ensure the script is in your PATH or the current directory.")
        return False

def get_script_path(codec):
    """Returns the path to the corresponding script for the given codec."""
    if codec.upper() == "HEVC":
        return "./encode_hevc_single.sh"
    elif codec.upper() == "JPEG":
        return "./encode_jpeg_single.py"
    elif codec.upper() == "AVC":
        return "./encode_avc_single.sh"
    else:
        return None

def main():
    """
    Main function to parse arguments and run the compression pipeline.
    """
    parser = argparse.ArgumentParser(description="Integrated Image/Video Compression Pipeline Software")
    
    parser.add_argument("--codec", required=True, help="Codec to use (e.g., HEVC, JPEG)")
    parser.add_argument("--QP", required=True, type=int, help="Quantization Parameter or JPEG Quality")
    parser.add_argument("--input", required=True, help="Path to the input file or directory")
    parser.add_argument("--output", required=True, help="Path to the output directory")
    parser.add_argument("--width", type=int, help="Frame width (required for HEVC codec)")
    parser.add_argument("--height", type=int, help="Frame height (required for HEVC codec)")
    parser.add_argument("--preset", default="medium", choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow", "slower", "veryslow"], help="FFmpeg encoding preset (default: medium)")
    parser.add_argument("--all_intra", action="store_true", help="Use All-Intra encoding (every frame is a keyframe)")

    args = parser.parse_args()



    logging.info("--- Compression Pipeline Started ---")
    log_message = f"Codec: {args.codec}, QP/Quality: {args.QP}, Input: {args.input}, Output: {args.output}"
    if args.width and args.height:
        log_message += f", Resolution: {args.width}x{args.height}"
    if args.width and args.height:
        log_message += f", Resolution: {args.width}x{args.height}"
    logging.info(log_message)

    script_path = get_script_path(args.codec)
    if not script_path:
        logging.error(f"Unsupported codec '{args.codec}'.")
        return

    if not os.path.exists(script_path):
        logging.error(f"Encoding script not found: '{script_path}'")
        return
    
    is_python_script = script_path.endswith('.py')
    if not is_python_script and not os.access(script_path, os.X_OK):
        logging.error(f"Script '{script_path}' is not executable. Please run 'chmod +x {script_path}'.")
        return

    input_path = args.input
    files_to_process = []
    if os.path.isfile(input_path):
        files_to_process.append(input_path)
    elif os.path.isdir(input_path):
        logging.info(f"Input is a directory. Processing files inside...")
        
        # Define supported extensions per codec
        video_extensions = ['.yuv', '.mp4', '.mov', '.avi', '.mkv']
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        
        target_extensions = []
        if args.codec.upper() in ['HEVC', 'AVC']:
            target_extensions = video_extensions
        elif args.codec.upper() == 'JPEG':
            target_extensions = image_extensions
            
        for filename in sorted(os.listdir(input_path)):
            if any(filename.lower().endswith(ext) for ext in target_extensions):
                files_to_process.append(os.path.join(input_path, filename))
            else:
                # Optional: Log skipped files if needed, or just silently skip
                pass
    else:
        logging.error(f"Input path is not a valid file or directory: {input_path}")
        return

    if not files_to_process:
        logging.warning("No files to process.")
        return
        
    os.makedirs(args.output, exist_ok=True)

    for file_path in files_to_process:
        logging.info(f"Processing file: '{file_path}'...")
        
        base_filename = os.path.basename(file_path)
        if args.codec.upper() == 'JPEG':
            base_filename = f"{os.path.splitext(base_filename)[0]}.jpg"
        elif args.codec.upper() == 'AVC':
            base_filename = f"{os.path.splitext(base_filename)[0]}.mp4"
        elif args.codec.upper() == 'HEVC':
            base_filename = f"{os.path.splitext(base_filename)[0]}.mp4"
        output_file_path = os.path.join(args.output, base_filename)

        command = []
        if is_python_script:
            command = [
                "python3", script_path,
                "--quality", str(args.QP),
                "--input", file_path,
                "--output", output_file_path
            ]
        else: # It's a shell script
            command = [
                script_path,
                "--qp", str(args.QP),
                "--input", file_path,
                "--output", output_file_path
            ]
            if args.codec.upper() == "HEVC" or args.codec.upper() == "AVC":
                command.extend(["--preset", args.preset])
                if args.all_intra:
                    command.append("--all_intra")
                if args.width and args.height:
                    command.extend(["--width", str(args.width), "--height", str(args.height)])
            


        run_command(command)

    logging.info("--- Compression Pipeline Finished ---")

if __name__ == "__main__":
    main()
