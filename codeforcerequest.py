import json


import requests


def request_find_problem(tags, rating):
    return rating
    url = f"https://codeforces.com/api/problemset.problems?tags={tags[:tags.find(';')]}"
    response = requests.get(url).json()
    print(response['result'])
    with open('request.json', 'w') as outfile:
        json.dump(response, outfile)
    if response['status'] == 'OK':
        s = []
        for el in response['result']['problems']:
            if 'rating' in el and el['rating'] == rating:
                s.append(el)
                break
    return f'''https://codeforces.com/problemset/problem/{s[-1]['contestId']}/{s[-1]['index']}'''
