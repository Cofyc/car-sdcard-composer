#!/bin/bash

USER=$(whoami)
FROM="/Users/${USER}/Music/iTunes/iTunes Music/"

echo "USER: $USER"
echo "FROM: $FROM"
echo ""

rsync -av --progress "$FROM" ./Musics/ \
    --exclude "/Podcasts" \
    --exclude "/Automatically Add to iTunes" \
    --exclude "/Downloads" \
    --exclude "/Home Videos" \
    --exclude "/Voice Memos" \
    --exclude "/Automatically Add to iTunes"

./convert.py ./Musics/
