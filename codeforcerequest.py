import json
from random import choice

import requests


def request_find_problem(tags, rating):
    print(tags, rating)
    url = f"https://codeforces.com/api/problemset.problems?tags={tags[0]}"
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

def my_profile_info(handle):
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url).json()
    profile = response['result'][0]
    answer = ''
    keys = ['handle', 'email', 'firstName', 'lastName', 'country', 'organization', 'rating', 'avatar']
    for key in keys[:-1]:
        if key in profile:
            answer += f'{key}: {profile[key]}\n'
    return answer