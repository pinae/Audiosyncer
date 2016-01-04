from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np

sound = AudioFileClip("sample_mono.mp3")
a = sound.to_soundarray()
print(a)
c2 = AudioArrayClip(a, fps=44100)
c2.write_audiofile("test.wav")

