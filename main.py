import os
import sys
import time
from colorama import Fore, Style, init
from moviepy.editor import VideoFileClip
from audio.diarize import diarize
from openai import OpenAI
import pandas as pd
from rich.console import Console
from rich.markdown import Markdown
import sys

console = Console()

# Initialize Colorama for cross-platform colored text
init(autoreset=True)

# ASCII Art Header for DebateZero
top_half = r""" ________  _______   ________  ________  _________  _______           ___ ________  _______   ________  ________     
|\   ___ \|\  ___ \ |\   __  \|\   __  \|\___   ___\\  ___ \         /  /|\_____  \|\  ___ \ |\   __  \|\   __  \    
\ \  \_|\ \ \   __/|\ \  \|\ /\ \  \|\  \|___ \  \_\ \   __/|       /  // \|___/  /\ \   __/|\ \  \|\  \ \  \|\  \   
 \ \  \ \\ \ \  \_|/_\ \   __  \ \   __  \   \ \  \ \ \  \_|/__    /  //      /  / /\ \  \_|/_\ \   _  _\ \  \\\  \ """
bot_half = r"""\ \  \_\\ \ \  \_|\ \ \  \|\  \ \  \ \  \   \ \  \ \ \  \_|\ \  /  //      /  /_/__\ \  \_|\ \ \  \\  \\ \  \\\  \ 
   \ \_______\ \_______\ \_______\ \__\ \__\   \ \__\ \ \_______\/_ //      |\________\ \_______\ \__\\ _\\ \_______\
    \|_______|\|_______|\|_______|\|__|\|__|    \|__|  \|_______|__|/        \|_______|\|_______|\|__|\|__|\|_______|"""
CYBERPUNK_BANNER = f"""
{Fore.CYAN} {top_half}
 {Fore.MAGENTA} {bot_half} 
{Fore.YELLOW}\t\t\t\t========== The Future of Debate Analysis ============{Fore.RESET}
"""


def cyberpunk_print(text, color, delay=0.02):
    """Print text with a cyberpunk typewriter effect."""
    for char in text:
        sys.stdout.write(color+char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def show_welcome_screen():
    """Display the welcome screen with banner and description."""
    os.system('cls' if os.name == 'nt' else 'clear')
    terminal_width = os.get_terminal_size().columns
    print(CYBERPUNK_BANNER)
    cyberpunk_print(f"Welcome to DebateZero, the cutting-edge debate analysis tool.", Fore.GREEN)
    cyberpunk_print(f"Input a debate clip and receive detailed info on any parameter you could dream of.", Fore.MAGENTA)
    print(f"{Fore.YELLOW}----------------------------------------------------------")
    print()


def ask_question(question, data_structure):
    prompt = "Here's a transcript of a debate:\n\n"
    for entry in data_structure:
        prompt += f"[{entry['speaker']}: {entry['content']}\n"
    prompt += f"\nQuestion: {question}"
    client = OpenAI(api_key = 'sk-3GLJ_C5EMvAHL1nfEzoybWVhNUaycNEyHrHMDfqJKhT3BlbkFJksK40un-Oshf1SyF1JXEDh_Z47_ExQ7NoXqoPzewsA')
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        # {"role": "system", "content": "You are a helpful assistant who is aware of the 2024 election between Donald Trump and Kamala Harris. You are also aware of how presidential debates work and understand the potential bias in such debates hosted by news networks."},
        {
            "role": "user",
            "content": prompt
        }
    ]
    )

    return completion.choices[0].message.content

def create_data_structure_from_csv(csv_path, face_eyes_ear_path, frame_interval=30):
    df = pd.read_csv(csv_path, delimiter=',', header=None, names=['start_time', 'end_time', 'content', 'Speaker'])
    df_ear = pd.read_csv(face_eyes_ear_path, delimiter=',', header=0, names=['Frame', 'Left EAR', 'Right EAR'])
    # print(df.head())

    # Initialize the list of dictionaries
    data_structure = []

    # Iterate over each row to create a dictionary for each line
    for index, row in df.iterrows():
        # print(index, row)
        # break
        # video_path = f"output_segments1/0{index}.mp4" 
        # base64Frames = video_to_base64_array(video_path)

        # if(idx==0): cv2.imwrite('test.jpg', base64_to_image(base64Frames[0]))

        segment_ear_data = df_ear[df_ear['Frame'].between(index * frame_interval, (index + 1) * frame_interval - 1)]
        avg_left_ear = segment_ear_data['Left EAR'].mean()  # Average EAR for the left eye
        avg_right_ear = segment_ear_data['Right EAR'].mean()

        entry = {
            'content': row['content'],
            'speaker': row['Speaker'],
            'left_ear': avg_left_ear,
            'right_ear': avg_right_ear,
            # 'image': base64Frames
        }
        data_structure.append(entry)
    # print(base64Frames[0].shape)
    return data_structure

def get_video_file():
    """Prompt the user to input the video file path."""
    video_path = input(f"{Fore.CYAN}Enter the path to your video file: {Fore.RESET}").strip()
    if not os.path.exists(video_path):
        cyberpunk_print(f"Error: File not found! Please check the path and try again.", Fore.RED)
        sys.exit(1)

    transcript_b = input(f"{Fore.CYAN}Would you like to diarize and transcribe this?(Y/n): {Fore.RESET}")
    if(transcript_b.lower() == 'y'):
        diarize(video_path)
        transcript_path = "transcript.srt"
    else:
        transcript_path = input(f"{Fore.GREEN}Enter transcript path: {Fore.RESET}").strip()
        if not os.path.exists(transcript_path):
            cyberpunk_print(f"Error: File not found! Please check the path and try again.", Fore.RED)
            sys.exit(1)
    return video_path, transcript_path


def process_video(video_path, transcript_path):
    """Process the video and return timestamps and information."""
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        print(f"{Fore.CYAN}{video_path} {Fore.RESET}({duration:.2f} seconds)")
        cyberpunk_print(f"Processing video: ", Fore.YELLOW)

        # Placeholder for future processing implementation
        # cyberpunk_print(f"Analyzing video...", Fore.MAGENTA)


        # clip_data = [
        #     {"timestamp": "00:00:10", "info": "Intro scene"},
        #     {"timestamp": "00:02:35", "info": "Key argument start"},
        #     {"timestamp": "00:05:20", "info": "Counter-argument presented"},
        #     {"timestamp": "00:08:15", "info": "Rebuttal section"}
        # ]

        ds = create_data_structure_from_csv(transcript_path, "face_eyes_ear.csv")
        # console.print(Markdown(ask_question("Note any interesting observations on tone of trump, harris, and the moderator", ds)))
        print(f"{Fore.CYAN}-"*192)
        # console.print(Markdown(ask_question("compare the EAR values between harris, trump, and moderator. what insights do you find? be quantitative", ds)))
        print(f"{Fore.CYAN}-"*192)
        # Spectral Analysis
        print(f"{Fore.CYAN}-"*192)

        while True:
            cyberpunk_print("Now, you ask a question: ", Fore.YELLOW)
            response = ask_question(input(f"{Fore.CYAN}-->{Fore.RESET}"), ds)
            console.print(Markdown(response))

        cyberpunk_print(f"Processing complete!", Fore.GREEN)
        # return clip_data

    except Exception as e:
        cyberpunk_print(f"Error processing video: {str(e)}", Fore.RED)
        sys.exit(1)


def display_results(clip_data):
    """Display the timestamps and information about the video clips."""
    print(f"\n{Fore.YELLOW}=== Results ===\n")
    for clip in clip_data:
        timestamp = clip['timestamp']
        info = clip['info']
        print(f"{Fore.CYAN}Timestamp: {Fore.RESET}{timestamp} {Fore.MAGENTA} | Info: {Fore.RESET}{info}")
    print()


def main():
    show_welcome_screen()

    # Get the video file from the user
    video_path, transcript_path = get_video_file()

    # Process the video and retrieve clip data
    process_video(video_path, transcript_path)

    # # Display the results
    # display_results(clip_data)


if __name__ == "__main__":
    main()
