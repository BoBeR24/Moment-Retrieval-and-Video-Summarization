import subprocess
import json
import os

def split_video_ffmpeg(input_file, output_dir, chunk_size=150):
    if not os.path.exists(input_file):
        print("File not found!")
        return

    # Create an output folder
    input_file_list = input_file.split('/')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Define the output pattern (e.g. chunk_000, chunk_001)
    base_name = input_file_list[-1].split(".")[0]
    output_pattern = os.path.join(output_dir, f"{base_name}_%03d.mp4")

    # The FFmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-force_key_frames', f'expr:gte(t,n_forced*{chunk_size})',  # inject keyframes
        '-f', 'segment',
        '-segment_time', str(chunk_size),
        '-c:v', 'libx264',  # must re-encode video to insert keyframes
        '-c:a', 'copy',  # audio can still be copied
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

def extract_video_segment(video_path, start_time, end_time, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)

    video_name = os.path.splitext(
        os.path.basename(video_path)
    )[0]

    output_path = os.path.join(
        output_dir,
        f"{video_name}_{start_time:.1f}_{end_time:.1f}.mp4"
    )

    duration = end_time - start_time

    subprocess.run([
        "ffmpeg",
        "-y",
        "-ss", str(start_time),
        "-i", video_path,
        "-t", str(duration),
        "-c", "copy",
        output_path
    ], check=True)

    return output_path


def extract_clips(input_file, output_file, timecodes):
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
        print("Processing clips...")
        subprocess.run(command, check=True)
        print(f"Video successfully saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def get_video_duration(input_file):
    """Fetches the duration of the video using ffprobe."""
    cmd = [
        'ffprobe', '-v', 'quiet', '-print_format', 'json',
        '-show_format', '-show_streams', input_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data['format']['duration'])


def adjust_video_speed(input_file, output_file, max_duration=150):
    duration = get_video_duration(input_file)

    if duration <= max_duration:
        print(f"Video is {duration:.2f}s. No adjustment needed.")
        # Simple copy to output if no change is needed
        subprocess.run(
            ['ffmpeg', '-y', '-i', input_file, '-c', 'copy', output_file],
            check=True
        )
        return 1

    # Calculate speed factor (e.g., 300s / 150s = 2.0x speed)
    speed_factor = duration / max_duration
    # setpts filter is the inverse of speed (1/speed_factor)
    pts_ratio = 1 / speed_factor # (basically a coefficient before the timestamp)

    # atempo filter has a limit of 2.0 per instance, so we chain them if needed
    filters = []
    temp_speed = speed_factor
    while temp_speed > 2.0:
        filters.append("atempo=2.0")
        temp_speed /= 2.0

    # Add the final remaining speed factor
    filters.append(f"atempo={temp_speed:.4f}")

    audio_filter = ",".join(filters)

    command = [
        'ffmpeg', '-i', input_file,
        '-filter_complex', f"[0:v]setpts={pts_ratio}*PTS[v];[0:a]{audio_filter}[a]",
        '-map', '[v]', '-map', '[a]',
        '-y', output_file
    ]

    try:
        print(f"Speeding up video by {speed_factor:.2f}x...")
        subprocess.run(command, check=True)
        print(f"Video is successfully sped up")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

    return speed_factor


def parse_timestamps(timestamps: str):
    if timestamps is None:
        return None

    start_time_str, end_time_str = timestamps.split(" - ")

    mins, secs = list(map(lambda x: int(x), start_time_str.split(":")))
    start_time = mins * 60 + secs

    mins, secs = list(map(lambda x: int(x), end_time_str.split(":")))
    end_time = mins * 60 + secs

    return float(start_time), float(end_time)
