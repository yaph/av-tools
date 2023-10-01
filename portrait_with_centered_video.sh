#/bin/bash
# Overlay a landscape video centered over a portrait image.
# portrait_with_centered_video.sh base-img.png video.mp4
set -eou pipefail

portrait=$1
video=$2

outdir=`dirname "$video"`
outfile=`basename "$video" mp4`portrait.mp4

ffmpeg -i $video -i $portrait \
    -filter_complex "[0:v]scale=1080:-1[video];[1:v][video]overlay=(W-w)/2:(H-h)/2:shortest=0[outv]" \
    -map "[outv]" -map 0:a -c:v libx264 -c:a copy "$outdir/$outfile"
