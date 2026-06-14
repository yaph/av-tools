#!/bin/bash
# Convert all WAV audio files in the current directory to MP3 format using the FFmpeg.
set -euo pipefail

for input in *.mp4; do
    output="${input%.*}".90."${input##*.}"
    ffmpeg -i "$input" -vf "transpose=2" "$output"
done