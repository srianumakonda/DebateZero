import cv2
import numpy as np
import os

def extract_frames_from_videos(video_paths, target_frame_count, fps):
    """Extract frames from multiple videos and ensure each video contributes the same number of frames."""
    all_videos_frames = []

    for video_path in video_paths:
        cap = cv2.VideoCapture(video_path)
        frames = []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Calculate frame interval to get the target frame count
        frame_interval = max(1, total_frames // target_frame_count)

        count = 0
        while cap.isOpened() and len(frames) < target_frame_count:
            ret, frame = cap.read()
            if not ret:
                break
            if count % frame_interval == 0:
                frames.append(frame)
            count += 1

        cap.release()

        # Ensure the frames list is of the target length
        if len(frames) < target_frame_count:
            frames += [frames[-1]] * (target_frame_count - len(frames))  # Repeat last frame if needed

        all_videos_frames.append(frames)

    return all_videos_frames

def create_grid_video(frames, grid_size, output_path, fps):
    """Create a video in a grid format from the extracted frames of multiple videos."""
    num_videos = len(frames)
    grid_height, grid_width = frames[0][0].shape[:2]
    output_height, output_width = grid_height * grid_size, grid_width * grid_size

    # Define the output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (output_width, output_height))

    # Iterate through frames and stitch them together in a grid
    for frame_idx in range(len(frames[0])):
        grid_frame = np.zeros((output_height, output_width, 3), dtype=np.uint8)
        
        for idx, video_frames in enumerate(frames):
            i, j = divmod(idx, grid_size)
            small_frame = video_frames[frame_idx]
            y1, y2 = i * grid_height, (i + 1) * grid_height
            x1, x2 = j * grid_width, (j + 1) * grid_width
            grid_frame[y1:y2, x1:x2] = small_frame
        
        # Write the grid frame to the output video
        out.write(grid_frame)

    out.release()

def main(input_folder, output_video_path):
    # Get the first 16 video files from the folder
    video_files = sorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov'))])[:16]

    if len(video_files) < 16:
        print("Not enough videos in the folder. At least 16 videos are required.")
        return

    # Extract frames from videos, ensuring each video is 3 seconds long at 30 fps
    fps = 30  # Frames per second
    duration_seconds = 3  # Output video duration in seconds
    target_frame_count = fps * duration_seconds

    frames = extract_frames_from_videos(video_files, target_frame_count, fps)

    # Create a 4x4 grid video
    grid_size = 4
    create_grid_video(frames, grid_size, output_video_path, fps)

if __name__ == "__main__":
    input_folder = "output_segments"  # Replace with your folder containing videos
    output_video_path = "output_gif_og.mp4"  # Output MP4 path
    main(input_folder, output_video_path)
    print("4x4 Grid Video created successfully!")

    input_folder = "output_segments1"  # Replace with your folder containing videos
    output_video_path = "output_gif_black.mp4"  # Output MP4 path
    main(input_folder, output_video_path)
    print("4x4 Grid Video created successfully!")

    input_folder = "output_segments2"  # Replace with your folder containing videos
    output_video_path = "output_gif_eyes.mp4"  # Output MP4 path
    main(input_folder, output_video_path)
    print("4x4 Grid Video created successfully!")
