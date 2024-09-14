from pydub import AudioSegment
from pyannote.audio import Pipeline
import re
import os
import datetime

def millisec(timeStr):
  spl = timeStr.split(":")
  s = (int)((int(spl[0]) * 60 * 60 + int(spl[1]) * 60 + float(spl[2]) )* 1000)
  return s

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
      start_time = datetime.strptime(start_time_str, '%H:%M:%S,%f')
      subtitles.append((start_time, index, time_range, subtitle_text))

  return subtitles


def write_srt(subtitles, output_file):
  with open(output_file, 'w', encoding='utf-8') as f:
    for i, (start_time, index, time_range, subtitle_text) in enumerate(sorted(subtitles), 1):
      f.write(f"{i}\n{time_range}\n{subtitle_text}\n\n")


def diarize(video_path):
  spacermilli = 2000
  spacer = AudioSegment.silent(duration=spacermilli)
  audio = AudioSegment.from_wav("testingaduio.wav")
  audio = spacer.append(audio, crossfade=0)
  audio.export('audio.wav', format='wav')
  pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization', use_auth_token="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")
  DEMO_FILE = {'uri': 'blabla', 'audio': 'audio.wav'}
  dz = pipeline(DEMO_FILE)
  with open("diarization.txt", "w") as text_file:
      text_file.write(str(dz))
  # print(*list(dz.itertracks(yield_label = True))[:10], sep="\n")
  dzs = open('diarization.txt').read().splitlines()
  groups = []
  g = []
  lastend = 0
  for d in dzs:
    if g and (g[0].split()[-1] != d.split()[-1]):      #same speaker
      groups.append(g)
      g = []
    g.append(d)
    end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=d)[1]
    end = millisec(end)
    if (lastend > end):       #segment engulfed by a previous segment
      groups.append(g)
      g = []
    else:
      lastend = end
  if g:
    groups.append(g)
  audio = AudioSegment.from_wav("audio.wav")
  gidx = -1


  for g in groups:
    start = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[0])[0]
    end = re.findall('[0-9]+:[0-9]+:[0-9]+\.[0-9]+', string=g[-1])[1]
    start = millisec(start)  # - spacermilli
    end = millisec(end)  # - spacermilli
    print(start, end)
    gidx += 1
    audio[start:end].export(str(gidx) + '.wav', format='wav')

  for i in range(gidx + 1):
    os.system(f"whisper {str(i) + '.wav'} --language en --model large")

  merged_subtitles = []
  for i in range(gidx + 1):
    merged_subtitles.extend(parse_srt(str(gidx)+".srt"))
  write_srt(merged_subtitles, "transcript.srt")
  # print(*groups, sep='\n')
