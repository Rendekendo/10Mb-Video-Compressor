import os
import subprocess
from tkinter import Tk, filedialog

def get_video_duration(file_path):
    """Get the duration of the video in seconds using FFmpeg."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        duration = float(result.stdout.strip())
        return duration
    except (ValueError, subprocess.SubprocessError):
        print("Error: Could not determine video duration. Please check the input file.")
        return None

def compress_video(input_path, output_path, target_size_mb):
    """Compress a video to fit within the target size."""
    # Get video duration
    duration = get_video_duration(input_path)

    # Safety margin to account for metadata and audio
    safety_margin = 0.90
    effective_target_size_mb = target_size_mb * safety_margin

    # Calculate target bitrate 
    target_bitrate_kbps = (effective_target_size_mb * 8192) / duration

    print(f"Target bitrate: {target_bitrate_kbps:.2f} kbps (with safety margin)")

    # Downscale resolution if necessary
    scale_filter = "scale=-2:720" 
    
    # Run FFmpeg command to compress the video
    command = [
        "ffmpeg", "-i", input_path,
        "-vf", scale_filter,  # Apply scaling
        "-b:v", f"{int(target_bitrate_kbps)}k",
        "-maxrate", f"{int(target_bitrate_kbps * 1.5)}k",
        "-bufsize", f"{int(target_bitrate_kbps * 2)}k",
        "-b:a", "96k",  # Reduce audio bitrate for additional space savings
        "-preset", "faster",
        "-c:v", "libx264",
        output_path
    ]

    subprocess.run(command)
    print(f"Compression complete! Saved to {output_path}")

def main():
    # Set up file dialog
    Tk().withdraw() 
    print("Drag and drop your video file into this window, or select it manually.")
    file_path = filedialog.askopenfilename(
        title="Select a Video File",
        filetypes=[("Video Files", "*.mp4 *.mov *.avi *.mkv *.flv")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return

    # Get output path
    base, ext = os.path.splitext(file_path)
    output_path = f"{base}_compressed{ext}"

    # Target size in MB
    target_size_mb = 10

    compress_video(file_path, output_path, target_size_mb)

if __name__ == "__main__":
    main()
