import string

import Reddit.structures
from Reddit import get_sub_reddit_top_posts, structures
from safe_speak import safe_speak as speak
import time


SUBREDDIT = 'askreddit'
TOP_POSTS_COUNT = 1
TOP_COMMENTS_COUNT = 30
DELAY = 2  # seconds


def read_post(reddit_post: Reddit.structures.Post, read_body=True, top_comments=0):
    title = reddit_post.get_title()
    body = reddit_post.get_self_text() if read_body else ""
    comments = reddit_post.get_top_comments(n=TOP_COMMENTS_COUNT) if top_comments > 0 else []

    speak(title)

    for i in split_sentences(body):
        for y in i.split("\n"):
            if any(x in y for x in string.ascii_letters):
                speak(y)


    for comment in comments:
        speak(comment.get_body())


def split_sentences(text: str, max_sentences=2) -> list:
    text_to_partition = text.split(".")
    while text_to_partition:
        data = " ".join(text_to_partition[:max_sentences]) + "."
        text_to_partition = text_to_partition[max_sentences:]
        if data.startswith(" "):
            data = data[1:]
        yield data


if __name__ == '__main__':
    posts = get_sub_reddit_top_posts(SUBREDDIT, TOP_POSTS_COUNT)

    for post in posts:
        read_post(post, read_body=True, top_comments=TOP_COMMENTS_COUNT)
