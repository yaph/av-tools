#!/bin/bash
# Encoding videos taken with the phone camera with ffmpeg significantly reduces file size,
# without visible loss of quality.
set -euo pipefail

mkdir -p optimized

for file in *; do
    if file --mime-type -b "$file" | grep -q "video"; then
        ffmpeg -i "$file" "optimized/$(basename "$file")"
    fi
done
