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

if __name__ == "__main__":
    split_video_ffmpeg("../TVSum/video_28.mp4")