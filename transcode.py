#!/usr/bin/env python3
import os
import sys
import glob
import subprocess
import psutil
import time
import json

# Reminder: set permissions to write to /Movies, /TV Shows, /Torrents

torrent_name = sys.argv[1]
torrent_full = '/home/Torrents/' + torrent_name

class Logger:
    def __init__(self, filename):
        self.outf = open(filename, 'a')
        self.record = ''
    def write(self, *args):
        s = ' '.join([str(i) for i in args])
        print(s)
        self.record += s + '\n'
    def save(self):
        self.outf.write(self.record)
        self.record = ''

log = Logger('/home/Torrents/log.txt')

def encode(inmov, outmov):
    log.write('Encoding movie ' + inmov + ' to ' + outmov)
    # cpu = psutil.cpu_percent(interval=3)
    # print('Current CPU: ', cpu)
    # while cpu > 50:
    #     print('Waiting until cpu usage decreases (' + str(cpu) + ')')
    #     sleep(300)
    #     cpu = psutil.cpu_percent(interval=0.5)
    
    # Parse input streams
    streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', inmov]).decode())['streams']
    # print('streams :', streams)
    filtered_codecs = ['hdmv_pgs_subtitle', 'mjpeg']
    filtered_streams = []
    for stream in streams:
        if 'codec_name' in stream and stream['codec_name'] in filtered_codecs:
            filtered_streams.append(stream['index'])
    log.write('Filtering streams', filtered_streams)
    filters = []
    for streamn in filtered_streams:
        filters.append('-map')
        filters.append('-0:' + str(streamn))
    
    # Transcode
    subprocess.check_output(['ffmpeg', '-i', inmov, '-map', '0', '-map', '-0:m:language:rus?', '-map', '-0:m:language:ukr?'] + filters + ['-vcodec', 'libx264', '-x264-params', 'analyse=none:ref=1:rc-lookahead=30', '-crf', '18', '-maxrate', '8M', '-bufsize', '8M', '-preset', 'fast', '-tune', 'film', '-filter:v', 'hqdn3d=0.0:0.0:3.0:3.0', '-acodec', 'aac', '-b:a', '256k', '-map_metadata', '-1', '-scodec', 'mov_text', '-movflags', 'faststart', outmov])
    log.save()

if os.path.isdir(torrent_full):
    # Torrent folder
    movies = []
    movies.extend(glob.iglob(torrent_full + '/**/*.mkv', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.mp4', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.avi', recursive=True))
    log.write('Movies: ', movies)
    
    torrent_name = torrent_name.replace('.', ' ')
    
    if len(movies) == 1:
        # Single movie
        out_prefix = '/home/Movies/' + torrent_name + '/'
        log.write('Movie identified, saving to ', out_prefix)
    else:
        # TV series
        out_prefix = '/home/TV Shows/' + torrent_name + '/'
        log.write('TV Series identified, saving to ', out_prefix)
        
        if not os.path.exists(out_prefix):
                os.makedirs(out_prefix)
        
    for movie in movies:
        movie_name = out_prefix + ' '.join(movie.split('/')[-1].split('.')[:-1]) + '.mp4'
        encode(movie, movie_name)
else:
    # Single file
    log.write('Single movie: ', torrent_full)
    movie_name = '/home/Movies/' + ' '.join(torrent_full.split('/')[-1].split('.')[:-1]) + '.mp4'
    encode(torrent_full, movie_name)

log.save()