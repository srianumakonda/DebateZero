# from pydub import AudioSegment
# from pyannote.audio import Pipeline
# import re
# import os
# import datetime

# def millisec(timeStr):
#   spl = timeStr.split(":")
#   s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
#   return s

# def parse_srt(file):
#   with open(file, 'r', encoding='utf-8') as f:
#     content = f.read().strip().split('\n\n')

#   subtitles = []
#   for block in content:
#     lines = block.split('\n')
#     if len(lines) >= 3:
#       index = lines[0]
#       time_range = lines[1]
#       subtitle_text = '\n'.join(lines[2:])
#       start_time_str = time_range.split(' --> ')[0]
#       start_time = datetime.strptime(start_time_str, '%H:%M:%S,%f')
#       subtitles.append((start_time, index, time_range, subtitle_text))

#   return subtitles


# def write_srt(subtitles, output_file):
#   with open(output_file, 'w', encoding='utf-8') as f:
#     for i, (start_time, index, time_range, subtitle_text) in enumerate(sorted(subtitles), 1):
#       f.write(f"{i}\n{time_range}\n{subtitle_text}\n\n")


# def diarize(video_path):
#   spacermilli = 2000
#   spacer = AudioSegment.silent(duration=spacermilli)
#   audio = AudioSegment.from_wav("output_audio.wav")
#   audio = spacer.append(audio, crossfade=0)
#   audio.export('audio.wav', format='wav')
#   pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")
#   DEMO_FILE = {'uri': 'blabla', 'audio': 'output_audio.wav'}
#   dz = pipeline(DEMO_FILE)
#   with open("diarization.txt", "w") as text_file:
#       text_file.write(str(dz))
#   # print(*list(dz.itertracks(yield_label = True))[:10], sep="\n")
#   dzs = open('diarization.txt').read().splitlines()
#   groups = []
#   g = []
#   lastend = 0
#   for d in dzs:
#     if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
#       groups.append(g)
#       g = []
#     g.append(d)
#     end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
#     end = millisec(end)
#     if (lastend > end):       #segment engulfed by a previous segment
#       groups.append(g)
#       g = []
#     else:
#       lastend = end
#   if g:
#     groups.append(g)
#   audio = AudioSegment.from_wav("audio.wav")
#   gidx = -1


#   for g in groups:
#     start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
#     end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
#     start = millisec(start)  # - spacermilli
#     end = millisec(end)  # - spacermilli
#     print(start, end)
#     gidx += 1
#     audio[start:end].export(str(gidx) + '.wav', format='wav')

#   for i in range(gidx + 1):
#     os.system(f"whisper {str(i) + '.wav'} --language en --model large")

#   merged_subtitles = []
#   for i in range(gidx + 1):
#     merged_subtitles.extend(parse_srt(str(gidx)+".srt"))
#   write_srt(merged_subtitles, "transcript.srt")
#   # print(*groups, sep='\n')

# diarize("video.mp4")

# from pydub import AudioSegment
# from pyannote.audio import Pipeline
# import re
# import os
# import datetime
# import subprocess

# # Convert time string to milliseconds
# def millisec(timeStr):
#     spl = timeStr.split(":")
#     s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
#     return s

# # Parse the srt file to extract information
# def parse_srt(file):
#     with open(file, 'r', encoding='utf-8') as f:
#         content = f.read().strip().split('\n\n')

#     subtitles = []
#     for block in content:
#         lines = block.split('\n')
#         if len(lines) >= 3:
#             index = lines[0]
#             time_range = lines[1]
#             subtitle_text = '\n'.join(lines[2:])
#             start_time_str = time_range.split(' --> ')[0]
#             start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S,%f')
#             subtitles.append((start_time, index, time_range, subtitle_text))

#     return subtitles

# # Write srt file
# def write_srt(subtitles, output_file):
#     with open(output_file, 'w', encoding='utf-8') as f:
#         for i, (start_time, index, time_range, subtitle_text) in enumerate(sorted(subtitles), 1):
#             f.write(f"{i}\n{time_range}\n{subtitle_text}\n\n")

# # Main function to perform diarization and transcription
# def detect_speech(video_path):
#     # Load audio file and add silence at the beginning to ensure smooth processing
#     spacermilli = 2000
#     spacer = AudioSegment.silent(duration=spacermilli)
#     audio = AudioSegment.from_file(video_path, format='mp4')
#     audio = spacer.append(audio, crossfade=0)
#     audio.export('audio.wav', format='wav')

#     # Load pre-trained speaker diarization model
#     pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="YOUR_HF_AUTH_TOKEN")
#     DEMO_FILE = {'uri': 'blabla', 'audio': 'audio.wav'}
#     diarization = pipeline(DEMO_FILE)

#     # Save diarization output to a file
#     with open("diarization.txt", "w") as text_file:
#         text_file.write(str(diarization))

#     # Process diarization results
#     dzs = open('diarization.txt').read().splitlines()
#     groups = []
#     g = []
#     lastend = 0

#     # Grouping segments by speakers
#     for d in dzs:
#         if g and (g[0].split()[-1] != d.split()[-1]):  # If it's the same speaker
#             groups.append(g)
#             g = []
#         g.append(d)
#         end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
#         end = millisec(end)
#         if (lastend > end):  # Segment engulfed by a previous segment
#             groups.append(g)
#             g = []
#         else:
#             lastend = end
#     if g:
#         groups.append(g)

#     # Extracting audio segments and transcribing them
#     audio = AudioSegment.from_wav("audio.wav")
#     gidx = -1
#     merged_subtitles = []

#     for g in groups:
#         start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
#         end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
#         start = millisec(start)
#         end = millisec(end)
#         print(start, end)
#         gidx += 1
#         audio[start:end].export(str(gidx) + '.wav', format='wav')

#         # Transcribe using Whisper
#         subprocess.run(f"whisper {str(gidx) + '.wav'} --language en --model large", shell=True)
#         srt_file = f"{str(gidx)}.srt"
#         parsed_subs = parse_srt(srt_file)
        
#         # Append speaker label to transcriptions
#         speaker_label = "Moderator" if "MOD" in g[0] else ("Trump" if "TRUMP" in g[0] else "Kamala Harris")
#         merged_subtitles.extend([(sub[0], sub[1], sub[2], f"{speaker_label}: {sub[3]}") for sub in parsed_subs])

#     # Write final merged srt
#     write_srt(merged_subtitles, "transcript.srt")

# # Run the function
# detect_speech("src/input_short.mp4")

import os
import re
import datetime
import subprocess
from pydub import AudioSegment
from pyannote.audio import Pipeline
from concurrent.futures import ThreadPoolExecutor

# Function to convert time string to milliseconds
def millisec(timeStr):
    spl = timeStr.split(":")
    s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2])) * 1000)
    return s

# Function to parse srt file to extract information
def parse_srt(file):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read().strip().split('\n\n')

    subtitles = []
    for block in content:
        lines = block.split('\n')
        if len(lines) >= 3:
            index = lines[0]
            time_range = lines[1]
            subtitle_text = '\n'.join(lines[2:])
            start_time_str = time_range.split(' --> ')[0]
            start_time = datetime.datetime.strptime(start_time_str, '%H:%M:%S,%f')
            subtitles.append((start_time, index, time_range, subtitle_text))

    return subtitles

# Function to write srt file
def write_srt(subtitles, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (start_time, index, time_range, subtitle_text) in enumerate(sorted(subtitles), 1):
            f.write(f"{i}\n{time_range}\n{subtitle_text}\n\n")

# Function to perform transcription using Whisper
def transcribe_with_whisper(audio_file):
    subprocess.run(f"whisper {audio_file} --language en --model small", shell=True)  # Use a smaller model for speed

# Main function to perform diarization and transcription
def detect_speech(video_path):
    # Prepare audio file
    audio = AudioSegment.from_file(video_path, format='mp4').set_frame_rate(16000).set_channels(1)  # Downsample and convert to mono
    audio.export('audio.wav', format='wav')

    # Load pretrained speaker diarization model
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")
    diarization = pipeline({'uri': 'blabla', 'audio': 'audio.wav'})

    # Save diarization output
    with open("diarization.txt", "w") as text_file:
        text_file.write(str(diarization))

    # Process diarization results
    dzs = open('diarization.txt').read().splitlines()
    groups, g, lastend = [], [], 0

    for d in dzs:
        if g and (g[0].split()[-1] != d.split()[-1]):
            groups.append(g)
            g = []
        g.append(d)
        end = millisec(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1])
        if lastend > end:
            groups.append(g)
            g = []
        else:
            lastend = end
    if g:
        groups.append(g)

    # Extract audio segments and run transcription in parallel
    audio = AudioSegment.from_wav("audio.wav")
    merged_subtitles = []
    with ThreadPoolExecutor(max_workers=4) as executor:  # Parallelize with 4 threads
        for gidx, g in enumerate(groups):
            start = millisec(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0])
            end = millisec(re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1])
            segment_file = f"{gidx}.wav"
            audio[start:end].export(segment_file, format='wav')
            executor.submit(transcribe_with_whisper, segment_file)

    # Merge transcriptions into a single SRT file
    for gidx in range(len(groups)):
        merged_subtitles.extend(parse_srt(f"{gidx}.srt"))
    write_srt(merged_subtitles, "transcript.srt")

# Run the function
detect_speech("src/input_short.mp4")
