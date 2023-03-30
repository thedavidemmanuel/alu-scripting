#!/usr/bin/python3
"""
Defines the count_words(subreddit, word_list) function.
"""

import requests


def count_words(subreddit, word_list, after="", words_count={}):
    """
    Queries the Reddit API and prints a sorted count of given keywords.

    subreddit: string representing the subreddit to search for
    word_list: list of strings representing the keywords to count
    after: string representing the post id to start searching after
    words_count: dictionary containing the count of each keyword

    Returns nothing.
    """
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "MyBot/0.0.1"}

    response = requests.get(url, headers=headers, allow_redirects=False, params={"after": after})

    if response.status_code == 200:
        data = response.json()["data"]
        after = data["after"]

        for child in data["children"]:
            title = child["data"]["title"].lower()
            for word in word_list:
                count = title.count(word.lower())
                if count > 0:
                    if word.lower() in words_count:
                        words_count[word.lower()] += count
                    else:
                        words_count[word.lower()] = count

        if after is None:
            if len(words_count) == 0:
                return
            for word, count in sorted(words_count.items(), key=lambda x: (-x[1], x[0])):
                print("{}: {}".format(word, count))
        else:
            count_words(subreddit, word_list, after, words_count)
    elif response.status_code != 404:
        return None
