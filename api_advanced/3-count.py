#!/usr/bin/python3
"""
3-count.py
"""
import sys
from collections import defaultdict
import requests

def count_words(subreddit, word_list, after=None, word_count=None):
    """
    A recursive function that queries the Reddit API, parses the title of all
    hot articles, and prints a sorted count of given keywords (case-insensitive,
    delimited by spaces).
    """
    if word_count is None:
        word_count = defaultdict(int)

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    if after:
        url += f"?after={after}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return

    data = response.json()

    for post in data["data"]["children"]:
        title = post["data"]["title"].lower()
        for word in word_list:
            word = word.lower()
            count = title.split().count(word)
            word_count[word] += count

    after = data["data"]["after"]

    if after:
        count_words(subreddit, word_list, after, word_count)
    else:
        sorted_count = sorted(
            [(k, v) for k, v in word_count.items() if v > 0],
            key=lambda x: (-x[1], x[0])
        )

        for word, count in sorted_count:
            print(f"{word}: {count}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])
