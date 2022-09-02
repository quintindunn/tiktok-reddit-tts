from __future__ import annotations

import json
import time

import requests
from .utilities import headers




class Post:
    def __init__(self, author_fullname, author, title, url, subreddit, ups, total_awards_received, score, created_utc,
                 comment_url, selftext):
        self.__author_fullname: str = author_fullname  # "author_fullname"
        self.__author: str = author  # "title"
        self.__title: str = title  # "title"
        self.__url: str = url  # "permalink"
        self.__subreddit: str = subreddit  # "subreddit"
        self.__ups: int = ups  # "ups"
        self.__total_awards_received: int = total_awards_received  # "total_awards_received"
        self.__score: int = score  # "score"
        self.__created_utc: int = created_utc  # "created"
        self.__comment_url: str = comment_url  # "url"
        self.__selftext: str = selftext  # "selftext"

        self.comments = None

    def get_top_comments(self, n=5) -> list[Comment]:
        comment_url_json = self.__comment_url + f".json?limit={n}"
        response = requests.get(comment_url_json, headers=headers)
        response.raise_for_status()
        return [Comment.from_dict(comment) for comment in response.json()[1]["data"]["children"][:n]]

    def get_title(self):
        return self.__title

    def get_author(self):
        return self.__author

    def get_self_text(self):
        return self.__selftext

    @staticmethod
    def from_dict(data: dict) -> Post:
        return Post(data["author_fullname"], data["author"], data["title"], data["permalink"], data["subreddit"],
                    data["ups"], data["total_awards_received"], data["score"], data["created"], data["url"], data["selftext"])


    def __str__(self):
        return f"{self.__author} - {self.__title}  -  {self.__ups}"

    def __repr__(self):
        return f"{self.__author}:{self.__title}..{self.__ups}"


class Comment:
    def __init__(self, author, body, ups, score, created_utc):
        self.__author: str = author
        self.__body: str = body
        self.__ups: int = ups
        self.__score: int = score
        self.__created_utc: int = created_utc

    @staticmethod
    def from_dict(data: dict) -> Comment:
        new_dict = data.copy()
        new_dict = new_dict["data"]
        try:
            return Comment(new_dict["author"], new_dict["body"], new_dict["ups"], new_dict["score"], new_dict["created"])
        except KeyError:
            print(new_dict)

    def get_author(self):
        return self.__author

    def get_body(self):
        return self.__body

    def get_ups(self):
        return self.__ups

    def get_score(self):
        return self.__score

    def get_created_utc(self):
        return self.__created_utc

    def __str__(self):
        return f"{self.__author}"

    def __repr__(self):
        return f"{self.__author}:{self.__body}..{self.__ups}"