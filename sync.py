from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np


def correlate(sample, base):
    fitness = []
    for offset in range(len(base) - len(sample)):
        window = base[offset:offset+len(sample)]
        fitness.append(np.sum((window - sample) ** 2))
    best_fitness = fitness[0]
    best_offset = 0
    for offset, f in enumerate(fitness):
        if f < best_fitness:
            best_fitness = f
            best_offset = offset
    return best_offset


def mix(offset, original, better):
    for i, sample in enumerate(original):
        if 0 <= i - offset < len(better):
            original[i] = better[i - offset]
    return original


if __name__ == "__main__":
    low_quality_sound = AudioFileClip("sample_mono.mp3")
    high_quality_sound = AudioFileClip("sample_mono.mp3")
    lqsa = low_quality_sound.to_soundarray()
    hqsa = high_quality_sound.to_soundarray()
    sample_start = 44100
    sample_len = 1000
    sample = hqsa[sample_start:sample_start+sample_len]
    offset = correlate(sample, lqsa) - sample_start
    print("Best offset: " + str(offset))
    good_sound = AudioArrayClip(mix(offset, lqsa, hqsa), fps=44100)
    good_sound.write_audiofile("test.wav")

