#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import ffmpeg

from collections import namedtuple
from pathlib import Path
from subprocess import run, list2cmdline


Coords = namedtuple('Coords', 'x y')
Dimensions = namedtuple('Dimensions', 'width height')


def get_dimensions(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return Dimensions(width=int(video_stream['width']), height=int(video_stream['height']))


def get_watermark_coords(video, watermark, position, margin):
    vid = get_dimensions(video)
    wm = get_dimensions(watermark)

    match position:
        case 'bl':
            return Coords(x=0 + margin, y=vid.height - (wm.height + margin))
        case 'br':
            return Coords(x=vid.width - (wm.width + margin), y=vid.height - (wm.height + margin))
        case 'tl':
            return Coords(x=0 + margin, y=0 + margin)
        case 'tr':
            return Coords(x=vid.width - (wm.width + margin), y=0 + margin)


parser = argparse.ArgumentParser(description='Add watermark image to video.')
parser.add_argument('video', type=str, help='The input video.')
parser.add_argument('watermark', type=str, help='The watermark image.')
parser.add_argument('-p', '--position', choices='bl br tl tr', default='br', help='Position of watermark.')
parser.add_argument('-m', '--margin', type=float, default=0, help='Margin to main image borders.')
cli_args = parser.parse_args()

p_video = Path(cli_args.video)
p_watermark = Path(cli_args.watermark)
p_output = p_video.parent.joinpath(f'{p_video.stem}.watermark{p_video.suffix}')

coords = get_watermark_coords(p_video, p_watermark, cli_args.position, cli_args.margin)

video = ffmpeg.input(p_video)
watermark = ffmpeg.input(p_watermark)

watermarked = ffmpeg.concat(video.overlay(watermark, x=coords.x, y=coords.y), video.audio, v=1, a=1).node
ffmpeg.output(watermarked[0], p_output.as_posix()).run()
