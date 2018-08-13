#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import psutil
import time

torrent_dir = sys.argv[1]
torrent_name = sys.argv[2]

torrent_full = torrent_dir + '/' + torrent_name

def encode(inmov, outmov):
    while psutil.cpu_percent() > 50:
        time.sleep(30)
    subprocess.check_output(['HandBrakeCLI', '-i', inmov, '-o', outmov, '-e', 'x264', '-q', '20', '-B', '160', '--encoder-preset', 'faster', '--all-subtitles', '-O', '--all-audio'])

if os.path.isdir(torrent_full):
    # Torrent folder
    movies = []
    movies.extend(glob.iglob(torrent_full + '/**/*.mkv', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.mp4', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.avi', recursive=True))
    
    if len(movies) == 1:
        # Single movie
        out_prefix = '/home/Movies/' + torrent_name + '/'
        subprocess.check_output(['mkdir', out_prefix])
    else:
        # TV series
        out_prefix = '/home/TV Shows/' + torrent_name + '/'
        subprocess.check_output(['mkdir', out_prefix])
    
    for movie in movies:
        movie_name = out_prefix + ''.join(movie.split('/')[-1].split('.')[:-1]) + '.mp4'
        encode(movie, movie_name)
else:
    # Single file
    movie_name = '/home/Movies/' + ''.join(torrent_full.split('/')[-1].split('.')[:-1]) + '.mp4'
    encode(torrent_full, movie_name)