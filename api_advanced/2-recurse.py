#!/usr/bin/python3
"""
    Recursive function that queries the Reddit API, and returns a list
    containing the titles of all hot articles for a given subreddit.
"""
import requests


def recurse(subreddit, hot_list=[], after=""):
    """
        Queries the Reddit API and returns a list containing the titles
        of all hot articles for a given subreddit.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params,
                            allow_redirects=False)

    if response.status_code != 200:
        return None

    data = response.json().get('data')
    if data is None:
        return None

    children = data.get('children')
    if children is None:
        return None

    for child in children:
        hot_list.append(child.get('data').get('title'))

    after = data.get('after')
    if after is None:
        return hot_list

    return recurse(subreddit, hot_list, after)
