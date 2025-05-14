# Audio Video Tools

Command line programs for processing audio and video created while working on https://ukealong.com/.

## Concatenate two video files omitting the audio

    ffmpeg -i v1.mp4 -i v2.mp4 -filter_complex "[0:v][1:v]concat=n=2:v=1:a=0[v]" -map "[v]" out.mp4

## Find Videos and Show Sizes

Find video files with and list their file sizes and the total size of all videos.

    find . -name "*.mp*" -print0 | du -shc --files0-from=-

## Fit Video

Fit a vertical video that is smaller than 1080x1920px on these dimensions:

    ffmpeg -i input.mp4 -vf "pad=1080:1920:(ow-iw)/2:(oh-ih)/2" output.mp4

## Remove Comments from MP3 files

    eyeD3 --remove-all-comments *.mp3

## Rotate Video

0 = 90 Counter Clockwise and Vertical Flip (default)
1 = 90 Clockwise
2 = 90 Counter Clockwise
3 = 90 Clockwise and Vertical Flip

    ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

## Speed-up Video

Speed up by a factor of 2.

    ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4
