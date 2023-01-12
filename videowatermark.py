#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import ffmpeg

from collections import namedtuple
from pathlib import Path


Coords = namedtuple('Coords', 'x y')
Dimensions = namedtuple('Dimensions', 'width height')


def get_dimensions(path):
    probe = ffmpeg.probe(path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)

    width = int(video_stream['width'])
    height = int(video_stream['height'])

    # Swap width and height if video is rotated
    if 'side_data_list' in video_stream:
        rot = video_stream['side_data_list'][0].get('rotation')
        if rot == -90:
            width, height = height, width

    return Dimensions(width=width, height=height)


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
parser.add_argument('-p', '--position', choices=['bl', 'br', 'tl', 'tr'], default='br', help='Position of watermark.')
parser.add_argument('-m', '--margin', type=float, default=0, help='Margin to main image borders.')
parser.add_argument('-s', '--silent', action='store_true', help='Set to silent if video hast no audio.')
argv = parser.parse_args()

p_video = Path(argv.video)
p_watermark = Path(argv.watermark)
p_output = p_video.parent.joinpath(f'{p_video.stem}.watermark{p_video.suffix}')

coords = get_watermark_coords(p_video, p_watermark, argv.position, argv.margin)

video = ffmpeg.input(p_video)
watermark = ffmpeg.input(p_watermark)

match argv.silent:
    case True:
        watermarked = ffmpeg.concat(video.overlay(watermark, x=coords.x, y=coords.y), v=1).node
    case _:
        watermarked = ffmpeg.concat(video.overlay(watermark, x=coords.x, y=coords.y), video.audio, v=1, a=1).node

ffmpeg.output(watermarked[0], p_output.as_posix()).run()
