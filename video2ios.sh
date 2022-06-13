#!/bin/bash
# Convert a video to a format that works on older versions of iOS.
set -euo pipefail

video=$1

out="${video%.*}"_ios."${video##*.}"

ffmpeg -i "$video" -vcodec libx264 -pix_fmt yuv420p -refs 11 -acodec aac "$out"