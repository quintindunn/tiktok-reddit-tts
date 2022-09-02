from unittest import TestCase
from text_to_speech import speak

from Reddit import get_sub_reddit_top_posts


class Test(TestCase):

    def test_tts(self):
        speak("Hello World")
        self.assertEqual("y", input("Did you hear me? (y/n)").lower())

    def test_get_sub_reddit_top_posts(self):
        posts = get_sub_reddit_top_posts("askreddit", n=2)
        self.assertEqual(2, len(posts))

        for post in posts:
            comments = post.get_top_comments(n=2)
            self.assertEqual(2, len(comments))
