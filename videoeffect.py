#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import time

from datetime import timedelta
from pathlib import Path
from subprocess import run, list2cmdline


START_TIME = time.time()
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
p_tmp = video_in.parent.joinpath(video_in.stem)
p_tmp.mkdir(exist_ok=True)
video_with_effect = p_tmp.joinpath(f'{cli_args.fx}.mp4')

# Split video into images
run(['ffmpeg', '-i', video_in, '-vf', f'fps={cli_args.fps}', f'{p_tmp}/%05d.png'])

# When passing the arguments as a list gmic fails with an 'Unknown filename' error.
cmd_gmic = f'gmic -input {p_tmp.joinpath("*.png")} {FX[cli_args.fx]} -output {video_with_effect},{cli_args.fps}'
run(cmd_gmic, shell=True)

# Merge orignal audio and video with effect
run(['merge_av.sh', video_in, video_with_effect])

# Done
print(f'Prgram execution time: {timedelta(seconds=time.time() - START_TIME)}')
run(['spd-say', 'finished'])