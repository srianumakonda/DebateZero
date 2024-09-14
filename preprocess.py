import cv2
import pandas as pd
import os

def time_to_frame_number(time_str, fps):
    """Convert a timestamp (in 'HH:MM:SS,sss' format) to a frame number."""
    try:
        # Split time by ':' and ','
        hours, minutes, seconds_ms = time_str.split(':')
        seconds, milliseconds = seconds_ms.split(',')
    except ValueError:
        raise ValueError(f"Time string format is incorrect: {time_str}")
    
    # Calculate total seconds
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds) + int(milliseconds) / 1000.0
    # Convert total seconds to frame number
    frame_number = int(total_seconds * fps)
    return frame_number

def split_video_by_timestamps(video_path, csv_path, output_dir):
    # Load the video
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read the CSV file without headers
    df = pd.read_csv(csv_path, delimiter=',', header=None, names=['start_time', 'end_time', 'content', 'Speaker'])

    # Ensure that start_time and end_time are strings
    df['start_time'] = df['start_time'].astype(str)
    df['end_time'] = df['end_time'].astype(str)

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each row in the CSV
    for index, row in df.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        speaker = row['Speaker']

        # Skip header row if it's accidentally included
        if start_time.lower().startswith("start_time"):
            continue
        
        # Convert start and end times to frame numbers
        start_frame = time_to_frame_number(start_time, fps)
        end_frame = time_to_frame_number(end_time, fps)

        # Set the video position to the start frame
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        # Create a VideoWriter object for the output video
        # output_file = os.path.join(output_dir, f'{speaker}_segment_0{index}.mp4')
        output_file = os.path.join(output_dir,f'0{index}.mp4')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        # Read frames and write to output video until the end frame is reached
        for frame_number in range(start_frame, end_frame + 1):
            ret, frame = video.read()
            if not ret:
                break
            out.write(frame)

        # Release the VideoWriter object
        out.release()
        print(f"Saved segment {index} for {speaker} from {start_time} to {end_time} as {output_file}")

    # Release the video capture object
    video.release()

if __name__ == "__main__":
    # video_path = "src/jan6.mp4"
    # csv_path = "src/jan6.csv"  # Ensure the path to your CSV file is correct
    # output_dir = "output_segments"
    # split_video_by_timestamps(video_path, csv_path, output_dir)

    video_path = "final/jan6_black_out.mp4"
    csv_path = "src/jan6.csv"  # Ensure the path to your CSV file is correct
    output_dir = "output_segments1"
    split_video_by_timestamps(video_path, csv_path, output_dir)

    # video_path = "final/jan6_eyes_out.mp4"
    # csv_path = "src/jan6.csv"  # Ensure the path to your CSV file is correct
    # output_dir = "output_segments2"
    # split_video_by_timestamps(video_path, csv_path, output_dir)