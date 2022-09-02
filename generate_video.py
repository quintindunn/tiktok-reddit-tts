import os

from video_edit import Video
from moviepy.editor import AudioFileClip, CompositeVideoClip
import random

from mutagen.mp3 import MP3

from config import *


def load_video(path):
    """
    Loads a video from a path.
    :param path: path to the video
    :return: video object
    """
    return Video(path)


def generate_segment(audio_playtime, video_length):
    """
    Generates a random segment of the video.
    :param audio_playtime: How long the audio is.
    :param video_length: How long the background video is.
    :return: start/end time
    """
    start = random.randint(0, int(video_length - audio_playtime))
    return start, start + audio_playtime


def generate(background_video, audio_playtime, text, output_path):
    background_clip = Video.from_path(background_video)
    start, end = generate_segment(audio_playtime, background_clip.clip.duration)
    background_clip.set_segment(start, end)


    clips = []
    for sentence, file in zip(text, list_tmp_dir_sorted()):
        clip_length = MP3(TMP_DIR + file).info.length
        clip_video = Video.from_scratch(clip_length, sentence)
        audio = AudioFileClip(TMP_DIR + file)
        clip_video.set_audio(audio)
        clip_video.save(TMP_DIR + file.replace(".mp3", ".webm"))
        clips.append(clip_video)

    background_clip.save(TMP_DIR + "background.webm")

    # args = [background_clip.clip] + [clip.clip for clip in clips]
    # final_clip = CompositeVideoClip(args, size=background_clip.clip.size, bg_color='black')
    # final_clip.write_videofile(output_path, fps=24, codec='libvpx')


def list_tmp_dir_sorted() -> list:
    """
    Lists the tmp directory sorted by their integer representation.
    :return: list of files in the tmp directory
    """
    files = os.listdir(TMP_DIR)
    return sorted(files, key=lambda x: int(x.split(".")[0]))


if __name__ == '__main__':
    load_video("background_videos/background.webm")
