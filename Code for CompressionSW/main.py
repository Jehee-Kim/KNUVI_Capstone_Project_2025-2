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
        return "./encode_avc.sh"
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
    parser.add_argument("--encoder_path", help="Path to the HEVC encoder executable (e.g., TAppEncoder)")

    args = parser.parse_args()

    if args.codec.upper() == "HEVC" and (not args.width or not args.height):
        logging.error("--width and --height arguments are required for the HEVC codec.")
        return

    logging.info("--- Compression Pipeline Started ---")
    log_message = f"Codec: {args.codec}, QP/Quality: {args.QP}, Input: {args.input}, Output: {args.output}"
    if args.width and args.height:
        log_message += f", Resolution: {args.width}x{args.height}"
    if args.encoder_path:
        log_message += f", Encoder: {args.encoder_path}"
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
        supported_extensions = ['.yuv', '.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.mov', '.avi']
        for filename in sorted(os.listdir(input_path)):
            if any(filename.lower().endswith(ext) for ext in supported_extensions):
                files_to_process.append(os.path.join(input_path, filename))
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
            if args.codec.upper() == "HEVC":
                command.extend(["--width", str(args.width), "--height", str(args.height)])
                if args.encoder_path:
                    command.extend(["--encoder_path", args.encoder_path])

        run_command(command)

    logging.info("--- Compression Pipeline Finished ---")

if __name__ == "__main__":
    main()
