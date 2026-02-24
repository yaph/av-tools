#!/usr/bin/env bash

set -e

if [ -z "$1" ]; then
  echo "Usage: $0 input_video"
  exit 1
fi

INPUT="$1"

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT"
  exit 1
fi

DIR="$(dirname -- "$INPUT")"
FILENAME="$(basename -- "$INPUT")"
EXT="${FILENAME##*.}"
NAME="${FILENAME%.*}"

OUTPUT="${DIR}/${NAME}.ig.${EXT}"

ffmpeg -i "$INPUT" \
  -vf "scale=1080:-2:flags=lanczos,pad=1080:608:(ow-iw)/2:(oh-ih)/2:black" \
  -c:v libx264 -profile:v high -level 4.1 -pix_fmt yuv420p \
  -crf 18 -preset slow \
  -movflags +faststart \
  -c:a aac -b:a 192k \
  "$OUTPUT"

echo "Created: $OUTPUT"
