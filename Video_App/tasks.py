import os
import subprocess

def convert_video_480p(source):
    file_name, _ = os.path.splitext(source)
    target = file_name + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    run = subprocess.run(cmd, capture_output=True)