import os
import subprocess


def delete_origin_mp4(linux_source):
    """
    Deletes the original MP4 file from the given path if it exists.

    Args:
    -----
    linux_source (str): The path of the MP4 file to be deleted.

    Process:
    --------
    - Checks if the file at `linux_source` exists.
    - If it exists, it is deleted.
    """
    if os.path.exists(linux_source):
        os.remove(linux_source)
    else:
        raise FileNotFoundError(f'The file "{linux_source}" does not exist.')


def convert_video(source, resolution, suffix):
    """
    Converts a video to HLS format with the given resolution and suffix.

    Args:
    -----
    source (str): The path to the source video.
    resolution (str): The resolution for the output video (e.g., 'hd480', 'hd720', 'hd1080').
    suffix (str): A suffix to append to the output file's name (e.g., '480p', '720p', '1080p').

    Process:
    --------
    - Constructs an `ffmpeg` command to convert the video to HLS format.
    - Runs the command using the `subprocess` module.
    - If successful, returns the target file path.


    Returns:
    --------
    str: The target HLS file path if successful, or `None` if the conversion fails.
    """
    file_name, _ = os.path.splitext(source)
    target = file_name + f'_{suffix}.m3u8'
    # cmd_hls = f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{target}"'
    cmd_hls = f'ffmpeg -i "{source}" -s {resolution} -c:v libx264 -crf 23 -c:a aac -strict -2 -start_number 0 -hls_time 10 -hls_list_size 0 -f hls "{target}" -threads 1'

    try:
        run = subprocess.run(cmd_hls, capture_output=True, shell=True)
        run.check_returncode()
        print(f"Video converted successfully to: {target}")
        return target
    except subprocess.CalledProcessError as e:
        print(f"Video converted not successfully to: {e}")
        print(f"FFmpeg output: {e.output}")
        print(f"FFmpeg stderr: {e.stderr}")
        return None


def convert_video_480p(source):
    """
    Converts a video to 480p HLS format.

    Args:
    -----
    source (str): The path to the source video.

    Returns:
    --------
    str: The target HLS file path if successful, or `None` if the conversion fails.
    """
    return convert_video(source, 'hd480', '480p')


def convert_video_720p(source):
    """
    Converts a video to 720p HLS format.

    Args:
    -----
    source (str): The path to the source video.

    Returns:
    --------
    str: The target HLS file path if successful, or `None` if the conversion fails.
    """
    return convert_video(source, 'hd720', '720p')


def convert_video_1080p(source):
    """
    Converts a video to 1080p HLS format and creates a master playlist.

    Args:
    -----
    source (str): The path to the source video.

    Process:
    --------
    - Converts the video to 1080p HLS format.
    - If successful, creates a master playlist including all resolutions.
    - Deletes the original MP4 file after conversion.

    Returns:
    --------
    None
    """
    linux_target = convert_video(source, 'hd1080', '1080p')
    if linux_target:
        create_master_playlist(os.path.dirname(linux_target), os.path.basename(source))
        delete_origin_mp4(source.replace('\\', '/'))


def create_master_playlist(target_directory, base_name):
    """
    Creates a master HLS playlist that includes 480p, 720p, and 1080p video streams.

    Args:
    -----
    target_directory (str): The directory where the playlist will be created.
    base_name (str): The base name of the video file (without extension).

    Process:
    --------
    - Writes the master playlist file with references to the 480p, 720p, and 1080p HLS streams.

    Returns:
    --------
    None
    """
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