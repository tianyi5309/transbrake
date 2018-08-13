#!/usr/bin/env python3
import os
import sys
import glob
import subprocess

torrent_dir = sys.argv[1]
torrent_name = sys.argv[2]

torrent_full = torrent_dir + '/' + torrent_name

if os.path.isdir(torrent_full):
    movies = []
    movies.extend(glob.iglob(torrent_full + '/**/*.mkv', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.mp4', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.avi', recursive=True))
    
    out_prefix = '/home/Movies/'
    if len(movies) > 1:
        out_prefix += torrent_name + '/'
        subprocess.check_output(['mkdir', out_prefix])
    
    for movie in movies:
        movie_name = out_prefix + movie.split('/')[-1].split('.')[0] + '.mp4'
        command = ['HandBrakeCLI', '-i', movie, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster']
        subprocess.check_output(command)
else:
    movie_name = '/home/Movies/' + movie.split('/')[-1].split('.')[0] + '.mp4'
    subprocess.check_output(['HandBrakeCLI', '-i', torrent_full, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster'])