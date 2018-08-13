#!/bin/sh
# echo "You shall not pass!" > /tmp/test.txt
# echo "$TR_TORRENT_DIR" > /tmp/dir.txt
# echo "$TR_TORRENT_NAME" > /tmp/name.txt
# which python3 > /tmp/py3ver.txt
python3 /home/Torrents/transbrake/transcode.py "$TR_TORRENT_DIR" "$TR_TORRENT_NAME"