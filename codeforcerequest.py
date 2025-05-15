import json
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

import requests


def request_find_problem(tags, rating):
    url = f"https://codeforces.com/api/problemset.problems?tags={tags[:tags.find(';')]}"
    response = requests.get(url).json()
    print(response['result'])
    with open('request.json', 'w') as outfile:
        json.dump(response, outfile)
    if response['status'] == 'OK':
        s = []
        for el in sorted(response['result']['problems'], reverse=True, key=lambda x: x['rating']):
            if el['rating'] == rating:
                s.append(el)
                break
    print(s)
