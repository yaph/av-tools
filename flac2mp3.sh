#!/bin/bash
# Convert all FLAC audio files in the current directory to MP3 format using the FFmpeg.
set -euo pipefail

for file in *.flac;
    do ffmpeg -i "$file" -vn "`basename "$file" flac`mp3";
done
