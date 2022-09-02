from __future__ import annotations

from moviepy.editor import VideoFileClip, TextClip


class Video:
    def __init__(self, clip):
        self.clip = clip

    @staticmethod
    def from_path(path) -> Video:
        return Video(VideoFileClip(path))

    @staticmethod
    def from_scratch(duration, text) -> Video:
        clip = TextClip(text, fontsize=25, color='white', bg_color='black')
        clip = clip.set_duration(duration)
        return Video(clip)

    def set_segment(self, start, end):
        self.clip = self.clip.subclip(start, end)
        return self.clip

    def mute_audio(self):
        self.clip.audio = None
        return self.clip

    def set_audio(self, audio):
        self.clip.audio = audio
        return self.clip

    def add_centered_text(self, text):
        self.clip = self.clip.text(text, fontsize=50, color='white',
                                   bg_color='black', x=(self.clip.w - 500) / 2, y=(self.clip.h - 50) / 2)
        return self.clip

    def save(self, path, fps=24):
        self.clip.write_videofile(path, fps=fps, codec='libvpx')
        return self.clip
