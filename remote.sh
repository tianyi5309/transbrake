#!/bin/sh
sleep 60
ssh -t root@b.tianyi.io "python3 /home/Torrents/transbrake/transcode.py '$TR_TORRENT_NAME'"
