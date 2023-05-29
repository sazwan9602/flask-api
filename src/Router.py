from flask import Flask, request
from . import Controller
from . import Utils

app = Flask(__name__)


@app.route('/')
def root():
    return "<a href='http://127.0.0.1:5000/top_posts' target='_blank'>Top Posts</a><br>" \
           "<a href='http://127.0.0.1:5000/search' target='_blank'>Search Filter</a>"


@app.route('/top_posts')
def top_posts():
    data = Controller.get_top_posts()
    response = Utils.APIResponse(data, 200, 'Success')
    return response.to_json()


@app.route('/search')
def search_comments():
    """
    search by post id [list or single id]
    search by keyword in name and body
    search by email
    :return:
    """
    data = Controller.filter_comments(request.args)
    response = Utils.APIResponse(data, 200, 'Success')
    return response.to_json()
