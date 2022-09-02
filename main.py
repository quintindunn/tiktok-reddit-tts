import os
import string

import Reddit.structures
from Reddit import get_sub_reddit_top_posts, structures
from safe_speak import safe_speak as speak
from mutagen.mp3 import MP3

import generate_video

from config import *


def split_sentences(text: str, max_sentences=2) -> list:
    """
    Splits text into sentences and returns a list of sentences.
    :param text: whole text to split
    :param max_sentences: max number of sentences before splitting
    :return: generator for strings of sentences
    """
    text_to_partition = text.split(".")
    while text_to_partition:
        data = " ".join(text_to_partition[:max_sentences]) + "."
        text_to_partition = text_to_partition[max_sentences:]
        if data.startswith(" "):
            data = data[1:]
        yield data


def setup_tmp():
    """
    Creates the tmp directory if it doesn't exist, if it does, it cleans the directory.
    :return:
    """
    import os
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)

    for file in os.listdir(TMP_DIR):
        os.remove(TMP_DIR + file)



def generate_audios(reddit_post: Reddit.structures.Post, read_body=True, top_comments=0):
    count = 0

    setup_tmp()

    data = []

    title = reddit_post.get_title()
    body = reddit_post.get_self_text() if read_body else ""
    comments = reddit_post.get_top_comments(n=TOP_COMMENTS_COUNT) if top_comments > 0 else []

    count += 1
    speak(title, save=True, file=f"tmp/{count}.mp3", speak=False)
    data.append(title)

    for i in split_sentences(body):
        for y in i.split("\n"):
            if any(x in y for x in string.ascii_letters):
                count += 1
                speak(y, save=True, file=f"tmp/{count}.mp3", speak=False)
                data.append(y)

    for comment in comments:
        count += 1
        speak(comment.get_body(), save=True, file=f"tmp/{count}.mp3", speak=False)
        data.append(comment.get_body())

    return data


def get_audio_playtime(count_delay=True):
    playtime = 0.0
    for file in os.listdir(TMP_DIR):
        playtime += MP3(TMP_DIR + file).info.length
        if count_delay:
            playtime += DELAY

    return playtime




if __name__ == '__main__':
    print("Getting posts...")
    posts = get_sub_reddit_top_posts(SUBREDDIT, TOP_POSTS_COUNT)


    for post in posts:
        print("Generating post, please wait...", end="")
        content = generate_audios(post, read_body=True, top_comments=TOP_COMMENTS_COUNT)
        audio_playtime = get_audio_playtime()
        print(f" Done, total audio playtime: {audio_playtime} seconds!")
        print("Generating video, please wait...", end="")
        generate_video.generate(BACKGROUND_VIDEO, audio_playtime, content, f"video.webm")
        print("Done!")
