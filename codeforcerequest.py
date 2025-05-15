import json
from random import choice

import requests


def request_find_problem(tags, rating):
    print(tags, rating)
    url = f"https://codeforces.com/api/problemset.problems?tags={tags[:tags.find(';')]}"
    response = requests.get(url).json()
    print(response['result'])
    with open('request.json', 'w') as outfile:
        json.dump(response, outfile)
    if response['status'] == 'OK':
        s = []
        for el in response['result']['problems']:
            if 'rating' in el and el['rating'] == int(rating):
                s.append(el)
    return f'''https://codeforces.com/problemset/problem/{choice(s)['contestId']}/{s[-1]['index']}'''
