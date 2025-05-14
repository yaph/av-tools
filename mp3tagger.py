#!/usr/bin/env python
from pathlib import Path
import argparse

import eyed3


parser = argparse.ArgumentParser(description="Tag MP3 files with metadata.")
parser.add_argument('directory', type=Path, help='Directory containing MP3 files to tag')
argv = parser.parse_args()

for file in argv.directory.glob('*.mp3'):
    artist, title = file.stem.split(' - ', maxsplit=1)
    audiofile = eyed3.load(file)

    # Update the tag if it doesn't exist or if the artist/title has changed
    set_tag = False
    if audiofile.tag is None:
        audiofile.initTag()
        set_tag = True
    elif audiofile.tag.artist != artist or audiofile.tag.title != title:
        set_tag = True
    if set_tag:
        print(f'Updating tag for {file.name}')
        audiofile.tag.artist = artist
        audiofile.tag.title = title
        audiofile.tag.album = None
        audiofile.tag.track = None
        audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')

    print(f'{file.stem}: {audiofile.tag.artist} - {audiofile.tag.title}')