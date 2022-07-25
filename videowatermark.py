#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import ffmpeg

from pathlib import Path
from subprocess import run, list2cmdline


parser = argparse.ArgumentParser(description='Add watermark image to video.')
parser.add_argument('video', type=str, help='The input video.')
parser.add_argument('watermark', type=str, help='The watermark image.')
# parser.add_argument('-fx', choices=FX.keys(), default='illustrationlook', help='Effect to apply.')
# parser.add_argument('-fps', type=float, default=25, help='Frames per seconds.')
# parser.add_argument('-c', '--continue', action='store_true', dest='CONTINUE', help='Continue a previously started process.')
cli_args = parser.parse_args()

p_video = Path(cli_args.video)
p_watermark = Path(cli_args.watermark)
p_output = p_video.parent.joinpath(f'{p_video.stem}.watermark{p_video.suffix}')

probe = ffmpeg.probe(p_video)
video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
width = int(video_stream['width'])
height = int(video_stream['height'])

# -i ~/repos/priv/ukealong/src/svg/screencast-overlay.svg \
#     -filter:a "volume=6dB" \
#     -filter_complex "[0:v][1:v] overlay=900:10" \
#     ~/Videos/ukealong/challenges/iimprovise/iimprovise-1.mp4

video = ffmpeg.input(p_video)
watermark = ffmpeg.input(p_watermark)

watermarked = ffmpeg.concat(video.overlay(watermark), video.audio, v=1, a=1).node
ffmpeg.output(watermarked[0], p_output.as_posix()).run()