#!/bin/bash
# ./merge_av.sh audio.mp3 video.mp4
set -euo pipefail

audio=$1
video=$2

filename=$(basename -- "$video")
out="${filename%.*}"_audio_merged."${filename##*.}"

ffmpeg -i "$audio" -i "$video" -c:v copy -c:a aac -map 0:a:0 -map 1:v:0 "$out"