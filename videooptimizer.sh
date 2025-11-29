#!/bin/bash
# Encoding videos taken with the phone camera with ffmpeg significantly reduces file size,
# without visible loss of quality.
set -uo pipefail

mkdir -p optimized

for file in *; do
    if file --mime-type -b "$file" | grep -q "video"; then
        base_name=$(basename "$file" | sed 's/\.[^.]*$//')
        output_file="optimized/${base_name}.mp4"

        # Skip if output already exists
        if [[ -f "$output_file" ]]; then
            echo "Skipping $file - output already exists"
            continue
        fi

        # Check if the input file is already encoded with libx265
        if ffprobe -v error -show_streams -select_streams v "$file" | grep -q "codec_name=hevc"; then
            echo "Skipping $file - already encoded with libx265"
            continue
        fi

        # Process with error handling
        if ffmpeg -i "$file" -c:v libx265 -preset slow -c:a copy "$output_file"; then
            # Keep modified time of original video
            touch -r "$file" "$output_file"
            echo "Converted: $file -> $output_file"
        else
            echo "Failed to convert: $file"
            [[ -f "$output_file" ]] && rm "$output_file"
        fi
    fi
done