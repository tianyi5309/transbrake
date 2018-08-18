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
        self.filename = filename
        self.record = ''
    def write(self, *args):
        s = ' '.join([str(i) for i in args])
        print(s)
        self.record += s + '\n'
    def save(self):
        with open(self.filename, 'a') as f:
            f.write(self.record)
        self.record = ''

log = Logger('/home/Torrents/log.txt')
processed = Logger('/home/Torrents/processed.txt')

def encode(inmov, outdir, outname):
    outtmp = '/home/Torrents/tmp/' + outname
    outmov = outdir + outname
    log.write('Encoding movie ' + inmov + ' to ' + outmov)
    
    # Parse input streams
    streams = json.loads(subprocess.check_output(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', inmov]).decode())['streams']
    streams = sorted(streams, key=lambda k: k['index']) # sort streams by index
    
    chosen_streams_numbers = []
    # Video stream - first video stream
    for stream in streams:
        if stream['codec_type'] == 'video':
            chosen_streams_numbers.append(stream['index'])
            break
    
    # Audio stream - choose all non-russian/ukranian audio
    for stream in streams:
        if stream['codec_type'] == 'audio':
            banned_languages = ['ukr', 'rus']
            if stream['tags']['language'] not in banned_languages:
                chosen_streams_numbers.append(stream['index'])
    
    # All subtitles except for russian and ukranian
    for stream in streams:
        if stream['codec_type'] == 'subtitle':
            banned_languages = ['ukr', 'rus']
            banned_codecs = ['hdmv_pgs_subtitle']
            if stream['tags']['language'] not in banned_languages and stream['codec_name'] not in banned_codecs:
                chosen_streams_numbers.append(stream['index'])
    
    log.write('Selected streams = ', chosen_streams_numbers)
    chosen_streams = []
    for stream in chosen_streams_numbers:
        chosen_streams.extend(['-map', '0:'+str(stream)])
    
    # Wait for cpu usage to decrease
    cpu = psutil.cpu_percent(interval=0.5)
    log.write('Current CPU: ', cpu)
    while cpu > 50:
        log.write('Waiting until cpu usage decreases (' + str(cpu) + ')')
        time.sleep(300)
        cpu = psutil.cpu_percent(interval=0.5)
    
    # Transcode
    start = time.time()
    subprocess.check_output(['ffmpeg', '-i', inmov] + chosen_streams + ['-vcodec', 'libx264', '-profile:v', 'high', '-level', '4.2', '-pix_fmt', 'yuv420p', '-deinterlace', '-x264opts', 'analyse=none:rc-lookahead=30:crf-max=25:qpmax=34', '-refs', '4', '-crf', '18', '-maxrate', '8M', '-bufsize', '16M', '-preset', 'fast', '-tune', 'film', '-filter:v', 'hqdn3d=1:1:4:4',  '-acodec', 'aac', '-ac', '2', '-b:a', '192k', '-af', 'aresample=async=1000', '-scodec', 'mov_text', '-movflags', '+faststart', outtmp])
    subprocess.check_output(['mv', outtmp, outmov])
    end = time.time()
    elapsed = end - start
    elapsed //= 60
    processed.write(inmov, 'encoded to', outmov, 'in', '{}h{}m'.format(elapsed//60, elapsed%60))
    processed.save()

if os.path.isdir(torrent_full):
    # Torrent folder
    movies = []
    movies.extend(glob.iglob(torrent_full + '/**/*.mkv', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.mp4', recursive=True))
    movies.extend(glob.iglob(torrent_full + '/**/*.avi', recursive=True))
    movies.sort()
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
        movie_name = ' '.join(movie.split('/')[-1].split('.')[:-1]) + '.mp4'
        encode(movie, out_prefix, movie_name)
else:
    # Single file
    log.write('Single movie: ', torrent_full)
    movie_name = ' '.join(torrent_full.split('/')[-1].split('.')[:-1]) + '.mp4'
    encode(torrent_full, '/home/Movies/', movie_name)

log.save()