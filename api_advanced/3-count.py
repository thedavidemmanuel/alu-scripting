#!/usr/bin/python3
""" 3-count.py """
import requests


def count_words(subreddit, word_list, after="", count_dict=None):
    """ prints a sorted count of given keywords """

    if count_dict is None:
        count_dict = {}

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    request = requests.get(url,
                           params={'after': after},
                           allow_redirects=False,
                           headers={'User-Agent': 'Mozilla/5.0'})

    if request.status_code == 200:
        data = request.json()

        for topic in (data['data']['children']):
            for word in topic['data']['title'].split():
                for keyword in word_list:
                    if keyword.lower() == word.lower():
                        count_dict[keyword.lower()] = count_dict.get(keyword.lower(), 0) + 1

        after = data['data']['after']
        if after is None:
            sorted_dict = dict(sorted(count_dict.items(),
                                      key=lambda x: (-x[1], x[0])))
            for k, v in sorted_dict.items():
                print("{}: {}".format(k, v))
        else:
            count_words(subreddit, word_list, after, count_dict)
