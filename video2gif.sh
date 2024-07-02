#!/bin/bash
# Convert a video to a GIF file speeding it up by a factor of 2.
# By default adds some padding to the video.
set -euo pipefail

video=$1
video_size=${2:-800}
padding_size=${3:-10}

output="${video%.*}".gif

# Convert video to GIF
ffmpeg -i "$video" -vf "fps=10,setpts=0.5*PTS,scale=${video_size}-${padding_size}*2:-1:flags=lanczos,pad=width=iw+${padding_size}*2:height=ih+${padding_size}*2:x=${padding_size}:y=${padding_size}:color=black" -c:v gif "$output"

echo "Conversion complete. Output saved as $output"