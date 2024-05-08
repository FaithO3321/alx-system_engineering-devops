#!/usr/bin/python3
"""
Module for querying the Reddit API
"""
import requests


def recurse(subreddit, hot_list=[], after=None):
    """
    Returns list containing titles of all hot articles for a given subreddit.
    If no results are found for the given subreddit, the function returns None.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "MyRedditAPIPython/0.1"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code == 200:
        try:
            data = response.json()
            posts = data["data"]["children"]
            after = data["data"]["after"]
            for post in posts:
                hot_list.append(post["data"]["title"])

            if after is not None:
                return recurse(subreddit, hot_list, after)
            else:
                return hot_list
        except (KeyError, ValueError):
            return None
    else:
        return None
