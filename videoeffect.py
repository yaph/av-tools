#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

from datetime import timedelta
from pathlib import Path
from subprocess import run, list2cmdline


START_TIME = time.time()
IMG_PATTERN = '%05d.png'
TMP_VIDEO = 'with-effect.mp4'

# Video effects
FX = {
    'brushify': '7,0.25,4,64,25,12,0,2,4,0.2,0.5,30,1,1,1,5,0,0.2,1',
    'dreamsmooth': 'fx_dreamsmooth 3,1,1,0.8,0,0.8,1,24,0',
    'coloredpencils': 'fx_cpencil 0.7,20,20,2,2,1,0',
    'graphicboost': 'fx_graphic_boost4 1.25,2,0,0.15,14,0,1,0.5,0.45,2,0,0,0,1,1,1,0.5,0.45,1',
    'graphicnovel': 'fx_graphic_novelfxl 0,2,6,5,20,0,0.62,14,0,1,0.5,0.78,1.92,0,0,0,1,1,1,0.5,0.8,1.28',
    'highlightbloom': 'fx_highlight_bloom 90,60,60,30,20,0,50,50',
    'illustrationlook': 'fx_illustration_look 100,0,0,0,0'
}

parser = argparse.ArgumentParser(description='Apply effect on input video one frame at a time.')
parser.add_argument('input', type=str, help='The input video.')
parser.add_argument('-fx', choices=FX.keys(), default='illustrationlook', help='Effect to apply.')
parser.add_argument('-fps', type=float, default=25, help='Frames per seconds.')
cli_args = parser.parse_args()

video_in = Path(cli_args.input)
p_new = video_in.parent.joinpath(f'{video_in.stem}-{cli_args.fx}')
p_input = p_new.joinpath('input')
p_input.mkdir(exist_ok=True, parents=True)
p_output = p_new.joinpath('output')
p_output.mkdir(exist_ok=True)

# Split video into images
run(['ffmpeg', '-i', video_in, '-vf', f'fps={cli_args.fps}', f'{p_input}/{IMG_PATTERN}'])

# Process images and apply effect
for img in p_input.glob('*.png'):
    img_new = p_output.joinpath(img.name)
    if img_new.exists():
        continue
    # When passing the arguments as a list gmic fails with an 'Unknown filename' error.
    cmd_gmic = f'gmic -input {img} {FX[cli_args.fx]} -output {img_new}'
    run(cmd_gmic, shell=True)

# Create new video
video_out = p_output.joinpath('video.mp4')
run(['ffmpeg', '-i', f'{p_output}/{IMG_PATTERN}', '-r', f'{cli_args.fps}', video_out])

# Merge orignal audio and video with effect
run(['merge_av.sh', video_in, video_out])

# Done
print(f'Program execution time: {timedelta(seconds=time.time() - START_TIME)}')
run(['spd-say', 'finished'])