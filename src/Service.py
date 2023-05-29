import requests
from flask import abort


def get_posts():
    url = 'https://jsonplaceholder.typicode.com/posts'
    resp = requests.get(url)
    if resp.status_code != 200:
        abort(resp.status_code, 'Bad request')
    return resp.json()


def get_comments():
    url = 'https://jsonplaceholder.typicode.com/comments'
    resp = requests.get(url)
    if resp.status_code != 200:
        abort(resp.status_code, 'Bad request')
    return resp.json()
