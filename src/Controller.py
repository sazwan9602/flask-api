import pandas as pd
from . import Service
from flask import abort

TOP_POST_COLUMNS = {'id': 'post_id', 'title': 'post_title', 'body': 'post_body', 'counts': 'total_number_of_comments'}
FILTER_IDS = {'post_id': 'postId', 'id': 'id'}
FILTER_KEYWORDS = {'name': 'name', 'email': 'email', 'caption': 'body'}


def get_top_posts():
    """
    Process top posts based on number of comments
    Method:
        1. get posts and comments data from API
        2. convert to dataframe to proceed with filtering
        3. rename columns name
        4. sort descending order by number of comments
    :return:
    """
    data = []

    try:
        posts = Service.get_posts()
        comments = Service.get_comments()

        df_cmt = pd.DataFrame(comments)
        df_posts = pd.DataFrame(posts)
        df = df_cmt['postId'].value_counts().reset_index(name='counts')
        df = df_posts.merge(df, left_on='id', right_on='postId').reindex(columns=['id', 'title', 'body', 'counts'])
        df = df.rename(columns=TOP_POST_COLUMNS)
        json_data = df.to_dict(orient='records')
        data = sorted(json_data, key=lambda e: e['post_id'], reverse=True)
    except Exception as e:
        abort(500, 'Internal Server Error')

    return data


def filter_comments(args):
    """
    filter search comments
        - by id
        - by post_id
        - by email
        - by keyword in name
        - by keyword in body caption
    :param args: query params
    """
    comments = Service.get_comments()
    df_cmt = pd.DataFrame(comments)

    for k, v in args.items():
        if k in FILTER_IDS:
            df_cmt = filter_by_ids(df_cmt, k, v)
        elif k in FILTER_KEYWORDS:
            df_cmt = filter_keywords(df_cmt, k, v)
        else:
            continue

    json_data = df_cmt.to_dict(orient='records')
    return json_data


def filter_keywords(data, field, value):
    """
    filter keyword in 'body', 'name' and 'email' value
    :param data: Comments dataframe
    :param field: filter key
    :param value: filter value
    """
    k = FILTER_KEYWORDS[field]

    try:
        data = data[data[k].str.contains(value, case=False)]
    except Exception as e:
        abort(500, 'Internal Server Error')
    return data


def filter_by_ids(data, field, value):
    """
    filter integer id's in post_id and post id
    :param data: Comments dataframe
    :param field: filter key
    :param value: filter value
    """
    k = FILTER_IDS[field]
    try:
        value = eval(value)  # evaluate string (accept, {}, [], ',')
    except:
        abort(500, f'{field} contains non-integer elements.')

    if type(value) is int:
        val = [value]
    else:
        val = list(value)

    data = data.loc[data[k].isin(list(set(val)))]
    return data
