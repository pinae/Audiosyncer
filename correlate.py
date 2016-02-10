#!/usr/bin/python3
# -*- coding: utf-8 -*-

from moviepy.editor import *
from moviepy.audio.AudioClip import AudioArrayClip
import numpy as np
import re


def correlate_by_squared_difference(base, sample):
    fitness = []
    for offset in range(len(base) - len(sample)):
        window = base[offset:offset+len(sample)]
        fitness.append(np.sum((window - sample) ** 2))
    return np.argmin(np.array(fitness))


def mix(offset, original, better):
    for i, sample in enumerate(original):
        if 0 <= i - offset < len(better):
            original[i] = better[i - offset]
    return original


def correlate(clip_filename, audio, output_filename):
    match = re.search("^\w+\.(mp3|wav|flac|ogg)$", clip_filename, re.IGNORECASE)
    save_video = True
    if match:
        low_quality_sound = AudioFileClip(clip_filename)
        save_video = False
    else:  # The file seems to be a video
        video_clip = VideoFileClip(clip_filename)
        low_quality_sound = video_clip.audio
    high_quality_sound = AudioFileClip(audio)
    audio_fps = max(low_quality_sound.fps, high_quality_sound.fps)
    lqsa = low_quality_sound.to_soundarray(nbytes=4, buffersize=1000, fps=audio_fps)
    hqsa = high_quality_sound.to_soundarray(nbytes=4, buffersize=1000, fps=audio_fps)
    sample_len = 10000
    sample_start = max(0, np.argmax(hqsa[:, 1]) - sample_len // 2)
    sample = hqsa[sample_start:sample_start+sample_len]
    correlation = np.correlate(lqsa[:, 1], sample[:, 1])
    offset = np.argmax(correlation) - sample_start
    good_sound = AudioArrayClip(mix(offset, lqsa, hqsa), fps=audio_fps)
    if save_video:
        video_clip.audio = good_sound
        video_clip.write_videofile(output_filename,
                                   codec='mpeg4',
                                   bitrate='4000000',
                                   audio_codec='pcm_s32le',
                                   audio_fps=audio_fps,
                                   #audio_bitrate='500000',
                                   preset='superslow',
                                   threads=4)
    else:
        good_sound.write_audiofile(output_filename,
                                   codec='pcm_s32le')
