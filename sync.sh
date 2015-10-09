#!/bin/sh

FROM='/Users/cofyc/Music/iTunes/iTunes Music/'

rsync -av --progress "$FROM" ./Musics/ \
    --exclude "/Podcasts" \
    --exclude "/Automatically Add to iTunes" \
    --exclude "/Downloads" \
    --exclude "/Home Videos" \
    --exclude "/Voice Memos"

./convert.py ./Musics/
