#!/usr/bin/env python3
import os
import glob
import subprocess

torrent_dir = os.environ['TR_TORRENT_DIR']
torrent_name = os.environ['TR_TORRENT_NAME']

movies = []
movies.extend(glob.iglob(torrent_dir + '/**/*.mkv', recursive=True))
movies.extend(glob.iglob(torrent_dir + '/**/*.mp4', recursive=True))

out_prefix = '/home/Movies/'
if len(movies) > 1:
    out_prefix += torrent_name + '/'

for movie in movies:
    movie_name = out_prefix + movie.split('/')[-1].split('.')[0] + '.mp4'
    print('HandBrakeCLI', '-i', movie, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster')
    # subprocess.check_output(["rm", "sra-download-out/" + seq + ".fastq"])