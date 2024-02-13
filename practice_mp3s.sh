#!/bin/bash
# Create slowed down versions of an mp3 file maintaining the pitch for practicing songs.
set -euo pipefail

if [ $# -eq 0 ]; then
    echo "Usage: $0 <input>"
    exit 1
fi

input="$1"
dir=$(dirname "$input")
slug=$(basename "$input" .mp3)

# Make sure seq outputs the right format
LC_NUMERIC=en_US.UTF-8

for tempo in $(seq 0.9 -0.1 0.5)
do
    percent=$(echo "$tempo * 100 / 1" | bc)
    output="$dir/$slug-$percent-percent.mp3"
    ffmpeg -i $input -filter:a "rubberband=tempo=$tempo" $output
done
