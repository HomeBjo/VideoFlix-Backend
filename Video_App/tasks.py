import os
import subprocess


def delete_origin_mp4(linux_source):
    if os.path.exists(linux_source):
        print(f'The file "{linux_source}" exists.')
        os.remove(linux_source)
    else:
        print(f'The file "{linux_source}" does not exist.')



def convert_video(source, resolution, suffix):
    file_name, _ = os.path.splitext(source)
    target = file_name + f'_{suffix}.m3u8'
    cmd_hls = f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{target}"'
    
    print('linux_target', target)
    try:
        run = subprocess.run(cmd_hls, capture_output=True, shell=True)
        run.check_returncode()
        return target
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert: {file_name} into {suffix}")
        print(f"Error: {e}")
        return None 



def convert_video_480p(source):
    return convert_video(source, 'hd480', '480p')



def convert_video_720p(source):
    return convert_video(source, 'hd720', '720p')



def convert_video_1080p(source):
    linux_target = convert_video(source, 'hd1080', '1080p')
    if linux_target:
        create_master_playlist(os.path.dirname(linux_target), os.path.basename(source))
        delete_origin_mp4(source.replace('\\', '/'))



def create_master_playlist(target_directory, base_name):
    file_name, _ = os.path.splitext(base_name)
    master_playlist = os.path.join(target_directory, f"{file_name}_master.m3u8")
    with open(master_playlist, 'w') as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=1400000,RESOLUTION=854x480\n")
        f.write(f"{file_name}_480p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=2800000,RESOLUTION=1280x720\n")
        f.write(f"{file_name}_720p.m3u8\n")
        f.write("#EXT-X-STREAM-INF:BANDWIDTH=5000000,RESOLUTION=1920x1080\n")
        f.write(f"{file_name}_1080p.m3u8\n")
    print(f"Master playlist created at {master_playlist}")

