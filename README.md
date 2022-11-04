# Audio Video Tools

Command line programs for processing audio and video created while working on https://ukealong.com/.

## Rotate Video

    ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

    0 = 90 Counter Clockwise and Vertical Flip (default)
    1 = 90 Clockwise
    2 = 90 Counter Clockwise
    3 = 90 Clockwise and Vertical Flip

## Speed-up Video

Speed up by a factor of 2.

    ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4
