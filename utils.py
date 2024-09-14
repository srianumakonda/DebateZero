import ffmpeg
import subprocess

# def stitch_audio(input_raw, output_mp4):
#     try:
#         # Use ffmpeg to combine video from the annotated file with audio from the original file
#         command = [
#             'ffmpeg', '-i', output_mp4, '-i', input_raw,
#             '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
#             '-map', '0:v:0', '-map', '1:a:0', '-shortest', output_mp4
#         ]
#         subprocess.run(command, check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Error combining video and audio: {e}")

def stitch_audio(input_raw, input_video, output_mp4):
    """
    Combine audio from input_raw with the video from input_video and save as output_mp4.
    """
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