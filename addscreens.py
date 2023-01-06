#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Add start and/or end screen images to video.
import argparse

import ffmpeg

from pathlib import Path


def get_streams(video):
    streams = {}
    probe = ffmpeg.probe(video)

    for stream in probe['streams']:
        if stream['codec_type'] == 'audio':
            streams['a'] = stream
        elif stream['codec_type'] == 'video':
            streams['v'] = stream

    return streams


parser = argparse.ArgumentParser(description='Add start and/or end screen to video.')
parser.add_argument('video', type=str, help='The input video. Currently only works if the video has audio.')
parser.add_argument('-s', '--start', help='Start screen image.')
parser.add_argument('-sd', '--start-duration', type=float, default=1, help='Start screen duration in seconds.')
parser.add_argument('-e', '--end', help='End screen image.')
parser.add_argument('-ed', '--end-duration', type=float, default=4, help='End screen duration in seconds.')
parser.add_argument('-o', '--outfile', type=Path, help='Name of the output video file.')
#parser.add_argument('--silent', action='store_true', help='Set to silent if video hast no audio.')
argv = parser.parse_args()

concat = []
dummy = None
streams = get_streams(argv.video)
framerate = streams['v']['r_frame_rate']
video = ffmpeg.input(argv.video)
video_audio = None

# Create dummy input to use as audio track for screens
if 'a' in streams:
    dummy = ffmpeg.input(f'anullsrc=r={streams["a"]["sample_rate"]}:cl={streams["a"]["channel_layout"]}', f='lavfi', t=0.1)
    video_audio = video.audio
else:
    dummy = ffmpeg.input(f'anullsrc', f='lavfi', t=0.1)
    video_audio = dummy.audio


if argv.start:
    stream = ffmpeg.input(argv.start, loop=1, t=argv.start_duration, framerate=framerate)
    concat += [stream.video, dummy.audio]

concat += [video.video, video_audio]

if argv.end:
    stream = ffmpeg.input(argv.end, loop=1, t=argv.end_duration, framerate=framerate)
    concat += [stream.video, dummy.audio]


if not (outfile := argv.outfile):
    p = Path(argv.video)
    outfile = p.parent.joinpath(f'{p.name}.addscreens{p.suffix}')

cmd = ffmpeg.concat(*concat, v=1, a=1).output(outfile.as_posix())
cmd.run()

# p2 = ffmpeg.input(endscreen, loop=1, t=SCREEN_DURATION, framerate=video_stream['r_frame_rate'])
# ffmpeg.concat(p1.video, p1.audio, p2.video, screen.audio, v=1, a=1).output('out.mp4')#.run()
