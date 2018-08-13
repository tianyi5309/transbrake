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
        movie_name = out_prefix + vmovie.split('/')[-1].split('.')[0] + '.mp4'
        command = ['HandBrakeCLI', '-i', movie, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster']
        print(command)
        subprocess.check_output(command)
else:
    movie_name = '/home/Movies/' + vmovie.split('/')[-1].split('.')[0] + '.mp4'
    subprocess.check_output(['HandBrakeCLI', '-i', torrent_full, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster'])

# movies = []
# movies.extend(glob.iglob(torrent_dir + '/**/*.mkv', recursive=True))
# movies.extend(glob.iglob(torrent_dir + '/**/*.mp4', recursive=True))
# 
# out_prefix = '/home/Movies/'
# if len(movies) > 1:
#     out_prefix += torrent_name + '/'
# 
# for movie in movies:
#     movie_name = out_prefix + vmovie.split('/')[-1].split('.')[0] + '.mp4'
#     print('HandBrakeCLI', '-i', movie, '-o', movie_name, '-e', 'x265', '-q', '20', '-B', '160', '--encoder-preset', 'faster')
#     # subprocess.check_output(["rm", "sra-download-out/" + seq + ".fastq"])