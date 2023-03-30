#!/usr/bin/python3
""" 3-count.py """
import requests


def count_words(subreddit, word_list, after="", count=[]):
    """ prints a sorted count of given keywords """

    if after == "":
        count = [0] * len(word_list)

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    request = requests.get(url,
                           params={'after': after},
                           allow_redirects=False,
                           headers={'User-Agent': 'Mozilla/5.0'})

    if request.status_code == 200:
        data = request.json()

        for topic in (data['data']['children']):
            for word in topic['data']['title'].split():
                for i in range(len(word_list)):
                    if word_list[i].lower() == word.lower():
                        count[i] += 1

        after = data['data']['after']
        if after is None:
            result = [(word_list[i].lower(), count[i]) for i in range(len(word_list))]
            result = sorted(result, key=lambda x: (-x[1], x[0]))

            printed = set()
            for word, c in result:
                if c > 0 and word not in printed:
                    print("{}: {}".format(word, c))
                    printed.add(word)
        else:
            count_words(subreddit, word_list, after, count)
