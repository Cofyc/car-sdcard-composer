#!/bin/bash

USER=$(whoami)
FROM="/Users/${USER}/Music/iTunes/iTunes Music/"

echo "USER: $USER"
echo "FROM: $FROM"
echo ""

./batch.py from_backup ./Musics.synconly/

rsync -av --progress "$FROM" ./Musics.synconly/ \
    --exclude "/Podcasts" \
    --exclude "/Automatically Add to iTunes" \
    --exclude "/Downloads" \
    --exclude "/Home Videos" \
    --exclude "/Voice Memos" \
    --exclude "/Automatically Add to iTunes"

./batch.py convert ./Musics.synconly/
./batch.py rename ./Musics.synconly/

./batch.py to_backup ./Musics.synconly/
