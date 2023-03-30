#!/usr/bin/python3
"""
Recursive function that queries the Reddit API and returns a list containing
the titles of all hot articles for a given subreddit.
"""
import requests
from collections import defaultdict

def count_words(subreddit, word_list, count_dict=None, after=None):
    if count_dict is None:
        count_dict = defaultdict(int)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    params = {"limit": 100, "after": after}
    res = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if res.status_code != 200:
        return

    res = res.json()
    hot_posts = res.get("data").get("children")
    
    for post in hot_posts:
        words = post.get("data").get("title").lower().split()
        for word in words:
            if word in word_list:
                count_dict[word.lower()] += 1

    after = res.get("data").get("after")
    if after is None:
        sorted_dict = dict(sorted(count_dict.items(), key=lambda x: (-x[1], x[0])))
        for k, v in sorted_dict.items():
            print(f"{k}: {v}")
        return

    return count_words(subreddit, word_list, count_dict, after)
