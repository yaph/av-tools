#!/bin/bash
# Convert video files in the current directory to MP3 format using the FFmpeg.
set -euo pipefail

for file in *.{mp4,mkv,webm}; do

    fullname=$(basename "$file")
    filename="${fullname%.*}"

    if [ "$filename" == "*" ]
        then continue
    fi

    ffmpeg -i "$file" -vn "$filename".mp3

done