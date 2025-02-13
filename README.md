# Video Compressor

Compresses videos to size which can be upladed to discord (10Mb)

## Requirements
- Python installed on your system
- [ffmpeg](https://www.ffmpeg.org/download.html) installed and added to system PATH

## How to Use
1. Run the script.
2. Select a video file using the file dialog.
3. The compressed video will be saved in the same location as the original file with `_compressed` added to its name.

## Features
- Automatically calculates target bitrate for compression
- Downscales video resolution to 720p if necessary
- Reduces audio bitrate for better compression
- Uses FFmpeg for high-quality video compression

