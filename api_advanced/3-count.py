#!/usr/bin/python3
"""
Recursive function that queries the Reddit API, parses the title of all hot articles, and prints a sorted count of given
keywords.
"""
import requests


def count_words(subreddit, word_list, after='', count_dict={}):
    """
    Query Reddit API recursively, and prints a sorted count of given keywords

    Args:
        subreddit: Name of the subreddit to be searched
        word_list: List of keywords to count occurrences of
        after: Pagination token to retrieve additional pages of the search
        count_dict: Dictionary to store the count of each keyword

    Returns:
        Sorted count of given keywords
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
    url = 'https://www.reddit.com/r/{}/hot.json?limit=100&after={}'.format(subreddit, after)
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 404:
        return None

    data = response.json().get('data')
    children = data.get('children')
    after = data.get('after')

    for child in children:
        title = child.get('data').get('title').lower().split()

        for word in word_list:
            count_dict[word] = count_dict.get(word, 0) + title.count(word.lower())

    if after is None:
        sorted_words = sorted(count_dict.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            if count == 0:
                continue
            print("{}: {}".format(word, count))
        return sorted_words

    return count_words(subreddit, word_list, after, count_dict)
