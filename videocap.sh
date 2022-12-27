#!/bin/bash
# Capture and save an image file from a video frame.
set -euo pipefail

video=$1
starttime=${2:-'0:00'}

out="${video%.*}".webp

ffmpeg -ss "$starttime" -i "$video" -frames:v 1 -q:v 2 "$out"
