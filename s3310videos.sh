#!/bin/sh
# Convert video files taken with the Samsung S3310 phone to a format that
# supports audio playback in mplayer.
# Rotate by 90° to the right if rotate option was given.

tmp="tmp.avi"

for f in *.3gp
do

    name=`echo "$f" | cut -d'.' -f1`
    target=`echo "$name.avi"`

    if [ 'rotate' = $1 ] ; then
        ffmpeg -i $f -f avi $tmp
        mencoder -vf rotate=1 -o $target -oac mp3lame -ovc lavc $tmp
        rm $tmp
    else
        ffmpeg -i $f -f avi $target
    fi

done
