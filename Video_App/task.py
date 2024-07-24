import subprocess
import os


def convert_480p(source):
        base_name = os.path.splitext(source)[0]
        new_file = base_name + '_480p.mp4'
        print("Source file:", source)
        print("Output file:", new_file)
        cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        run = subprocess.run(cmd, capture_output=True)
        
        
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
        #  cmd = 'C:/usr/ffmpeg/bin/ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)