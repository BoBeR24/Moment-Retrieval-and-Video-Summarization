import subprocess
import os

def split_video_ffmpeg(input_file, chunk_size=150):
    if not os.path.exists(input_file):
        print("File not found!")
        return

    # Create an output folder
    input_file_list = input_file.split('/')
    output_dir = '/'.join(input_file_list[:-1]) + '/' + input_file_list[-1].split('.')[0] + "_chunks"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output pattern (e.g. chunk_000, chunk_001)
    base_name = input_file_list[-1].split(".")[0]
    output_pattern = os.path.join(output_dir, f"{base_name}_%03d.mp4")

    # The FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-f', 'segment',
        '-segment_time', str(chunk_size),
        '-c', 'copy',
        '-reset_timestamps', '1',
        output_pattern
    ]

    try:
        print(f"Splitting {input_file} into {chunk_size}s chunks...")
        subprocess.run(command, check=True)
        print(f"Chunks are successfully saved into '{output_dir}' folder.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    return output_dir


def extract_clips(input_file, output_file, timecodes):
    """
    Extracts multiple clips from a video and joins them into one.

    :param input_file: Path to the source video.
    :param output_file: Path for the final output.
    :param timecodes: List of tuples (start, end) in seconds or "HH:MM:SS".
    """

    filter_complex = ""
    inputs = ""

    for i, (start, end) in enumerate(timecodes):
        # Build the trim filters for video and audio
        filter_complex += (
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}]; "
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]; "
        )
        inputs += f"[v{i}][a{i}]"

    # Concatenate all the trimmed segments
    filter_complex += f"{inputs}concat=n={len(timecodes)}:v=1:a=1[outv][outa]"

    # Construct the FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-filter_complex', filter_complex,
        '-map', '[outv]',
        '-map', '[outa]',
        '-y',  # Overwrite output file if it exists
        output_file
    ]

    try:
        print("Processing clips... this may take a moment.")
        subprocess.run(command, check=True)
        print(f"Success! Video saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")



def parse_timestamps(timestamps: str):
    start_time_str, end_time_str = timestamps.split(" - ")

    mins, secs = list(map(lambda x: int(x), start_time_str.split(":")))
    start_time = mins * 60 + secs

    mins, secs = list(map(lambda x: int(x), end_time_str.split(":")))
    end_time = mins * 60 + secs

    return float(start_time), float(end_time)