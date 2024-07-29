import os
import subprocess

def convert_video_480p(source):
    file_name, _ = os.path.splitext(source)
    target = file_name + '_480p.mp4'
    linux_source = "/mnt/" + source.replace('\\', '/').replace('C:', 'c')
    linux_target = "/mnt/" + target.replace('\\', '/').replace('C:', 'c')
    print("linux_source is ", linux_source)
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(linux_source, linux_target)
    run = subprocess.run(cmd, capture_output=True, shell=True)
    
    #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)