#!/bin/bash
# Resize all MP4 in the current directory to a width of 640 and save them in `resized` directory.
set -euo pipefail

mkdir -p resized

for file in *.mp4;
    do ffmpeg -i "$file" -filter:v scale=640:-1 -c:a copy "resized/`basename "$file"`";
done