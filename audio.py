#!/usr/bin/env python3
# audio.py file delay
# Offsets audio by x seconds
import sys
import subprocess

movie = sys.argv[1]
delay = sys.argv[2]
# Generate copied file
subprocess.check_output(['ffmpeg', '-i', movie, '-itsoffset', delay, '-i', movie, '-map', '0', '-map', '-0:a', '-map', '1:a', '-codec', 'copy', 'out.mkv'])

subprocess.check_output(['mv', 'out.mkv', movie])