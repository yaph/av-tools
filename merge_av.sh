#!/bin/bash
# ./merge_av.sh audio.mp3 video.mp4
set -euo pipefail

audio=$1
video=$2

out="${video%.*}"_audio_merged."${video##*.}"

ffmpeg -i "$audio" -i "$video" -c:v copy -c:a aac -map 0:a:0 -map 1:v:0 "$out"