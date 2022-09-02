from text_to_speech import speak
import re
from .overwrites import overwrites


def add_overwrite(word, replacement):
    overwrites[word] = replacement


def safe_speak(text, print_text=True):
    for overwrite in overwrites:
        pattern = re.compile(overwrite, re.IGNORECASE)
        text = pattern.sub(overwrites[overwrite], text)
    if print_text:
        print(text)
    return speak(safe_for_tts(text))


def safe_for_tts(text):
    exception_overwrites = {
        "\"": "",
    }
    for overwrite in exception_overwrites:
        pattern = re.compile(overwrite, re.IGNORECASE)
        text = pattern.sub(exception_overwrites[overwrite], text)
    return text
