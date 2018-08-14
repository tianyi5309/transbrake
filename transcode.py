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
    print('Copying movie ' + inmov + ' to ' + outmov)
    subprocess.check_output(['ffmpeg', '-i', inmov, '-map', '0', '-map', '-0:m:language:rus?', '-map', '-0:m:language:ukr?', '-vcodec', 'copy', '-acodec', 'copy', '-scodec', 'mov_text', outmov])

    # subprocess.check_output(['mv', inmov, outmov]) # copy file
    # print('Encoding movie ' + inmov + ' to ' + outmov)
    # cpu = psutil.cpu_percent(interval=10)
    # print('Current CPU: ', cpu)
    # while cpu > 50:
        # print('Waiting until cpu usage decreases (' + str(cpu) + ')')
        # cpu = psutil.cpu_percent(interval=120)
    # subprocess.check_output(['HandBrakeCLI', '-i', inmov, '-o', outmov, '-e', 'x264', '-q', '16', '-B', '160', '--encoder-preset', 'fast', '--all-subtitles', '-O', '--all-audio'])

if os.path.isdir(torrent_full):
    # Torrent folder
    movies = []
    movies.extend(glob.iglob(torrent_full + '/**/*.mkv', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.mp4', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.avi', recursive=True))
    print('Movies: ', movies)
    
    torrent_name = torrent_name.replace('.', ' ')
    
    if len(movies) == 1:
        # Single movie
        out_prefix = '/home/Movies/' + torrent_name + '/'
        if not os.path.exists(out_prefix):
            os.makedirs(out_prefix)
    else:
        # TV series
        out_prefix = '/home/TV Shows/' + torrent_name + '/'
        if not os.path.exists(out_prefix):
            os.makedirs(out_prefix)
        
    for movie in movies:
        movie_name = out_prefix + ' '.join(movie.split('/')[-1].split('.')[:-1]) + '.mp4'
        encode(movie, movie_name)
else:
    # Single file
    print('Single movie: ', torrent_full)
    movie_name = '/home/Movies/' + ' '.join(torrent_full.split('/')[-1].split('.')[:-1]) + '.mp4'
    encode(torrent_full, movie_name)