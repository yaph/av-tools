#!/bin/bash
# This script combines a video file with no sound and an audio file using ffmpeg,
# ensuring that if the audio is longer, the last frame of the video is shown until the audio ends,
# and if the video is longer, silence follows after the audio finishes.
set -euo pipefail

# Check if correct number of arguments provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <audio> <video>"
    exit 1
fi

audio=$1
video=$2

out="${video%.*}".av."${video##*.}"

ffmpeg -i "$audio" -i "$video" -c:v copy -c:a aac -map 0:a:0 -map 1:v:0 "$out"