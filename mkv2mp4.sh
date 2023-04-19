#!/bin/bash
# Convert all MKV video files in the current directory to MP4 format using the FFmpeg.
set -euo pipefail

for i in *.mkv; do
    target=`basename -s mkv "$i"`
    ffmpeg -i "$i" -c:v copy -c:a opus -strict -2 "$target"mp4;
done
