import requests
from .utilities import headers
from .structures import Post


def get_sub_reddit_top_posts(subreddit: str, n=5) -> list[Post]:

    request_url = f"https://www.reddit.com/r/{subreddit}/top.json?limit={n}"
    response = requests.get(request_url, headers=headers)
    response.raise_for_status()
    posts = response.json()["data"]["children"]
    posts = [Post.from_dict(post["data"]) for post in posts]
    return posts

