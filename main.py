import os
import sys
import time
from colorama import Fore, Style, init
from moviepy.editor import VideoFileClip
from diarize import diarize

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


def get_video_file():
    """Prompt the user to input the video file path."""
    video_path = input(f"{Fore.CYAN}Enter the path to your video file: {Fore.RESET}")
    if not os.path.exists(video_path):
        cyberpunk_print(f"Error: File not found! Please check the path and try again.", Fore.RED)
        sys.exit(1)

    transcript_b = input(f"{Fore.CYAN}Would you like to diarize and transcribe this?(Y/n): {Fore.RESET}")
    if(transcript_b.lower() == 'y'):
        diarize(video_path)
        transcript_path = "transcript.srt"
    else:
        transcript_path = input(f"{Fore.GREEN}Enter transcript path: {Fore.RESET}")
        if not os.path.exists(transcript_path):
            cyberpunk_print(f"Error: File not found! Please check the path and try again.", Fore.RED)
            sys.exit(1)
    return video_path, transcript_path


def process_video(video_path, transcript_path):
    """Process the video and return timestamps and information."""
    try:
        clip = VideoFileClip(video_path)
        duration = clip.duration
        cyberpunk_print(f"Processing video: ", Fore.YELLOW)
        print(f"{Fore.CYAN}{video_path} {Fore.RESET}({duration:.2f} seconds)")

        # Placeholder for future processing implementation
        cyberpunk_print(f"Analyzing video...", Fore.MAGENTA)

        # Simulate processing time
        time.sleep(3)

        # Sample clip data to return (you can modify this)
        clip_data = [
            {"timestamp": "00:00:10", "info": "Intro scene"},
            {"timestamp": "00:02:35", "info": "Key argument start"},
            {"timestamp": "00:05:20", "info": "Counter-argument presented"},
            {"timestamp": "00:08:15", "info": "Rebuttal section"}
        ]

        cyberpunk_print(f"Processing complete!", Fore.GREEN)
        return clip_data

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
    video_path = get_video_file()

    # Process the video and retrieve clip data
    clip_data = process_video(video_path, transcript_path)

    # Display the results
    display_results(clip_data)


if __name__ == "__main__":
    main()
