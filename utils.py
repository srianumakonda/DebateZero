import ffmpeg
import numpy as np
import subprocess

def stitch_audio(input_raw, input_video, output_mp4):

    try:
        # Use ffmpeg to combine video from the annotated file with audio from the original file
        command = [
            'ffmpeg', '-i', input_video, '-i', input_raw,
            '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
            '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_mp4
        ]
        subprocess.run(command, check=True)
        print(f"Successfully combined video from {input_video} with audio from {input_raw} into {output_mp4}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining video and audio: {e}")

def euclidean_distance(point1, point2):
    return np.linalg.norm(np.array(point1) - np.array(point2))

def ear(eyes_arr):
    # Ensure eyes_arr has exactly 12 points (6 for each eye)
    assert len(eyes_arr) == 12, "eyes_arr must contain 12 landmarks (6 for each eye)."

    # Left eye landmarks: p1 to p6
    left_eye = eyes_arr[:6]
    # Right eye landmarks: p1 to p6
    right_eye = eyes_arr[6:]

    # Calculate EAR for the left eye
    left_ear = (euclidean_distance(left_eye[1], left_eye[5]) + euclidean_distance(left_eye[2], left_eye[4])) / (2.0 * euclidean_distance(left_eye[0], left_eye[3]))
    
    # Calculate EAR for the right eye
    right_ear = (euclidean_distance(right_eye[1], right_eye[5]) + euclidean_distance(right_eye[2], right_eye[4])) / (2.0 * euclidean_distance(right_eye[0], right_eye[3]))
    
    return left_ear, right_ear


def srt_time_to_seconds(srt_time):
    # Split into hours, minutes, seconds, and milliseconds
    hours, minutes, seconds = srt_time.split(':')
    seconds, milliseconds = seconds.split(',')

    # Convert each to float and sum to get total seconds
    total_seconds = (
        int(hours) * 3600 +  # Convert hours to seconds
        int(minutes) * 60 +  # Convert minutes to seconds
        int(seconds) +       # Add seconds
        int(milliseconds) / 1000  # Convert milliseconds to seconds
    )
    
    return total_seconds
