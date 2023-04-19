#!/bin/bash
# Convert all WAV audio files in the current directory to MP3 format using the FFmpeg.
set -euo pipefail

for i in *.wav; do
    out=`basename -s wav "$i"`
    ffmpeg -i "$i" -codec:a libmp3lame -qscale:a 2 "$out"
done