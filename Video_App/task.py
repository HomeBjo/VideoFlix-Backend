import subprocess
import os


def  convert_video_480p(source):
        video_name = os.path.splitext(source)[0]
        new_video_name = video_name + '_480p.mp4'
        cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_video_name)
        run = subprocess.run(cmd, capture_output=True)
        
        
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
