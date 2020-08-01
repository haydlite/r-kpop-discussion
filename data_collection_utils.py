import requests
import json
import pickle
import logging
import os
import time

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux ppc64le; rv:75.0) Gecko/20100101 Firefox/75.0'}

def collect_posts(min_score = 50, min_num_comments = 50, request_size = 50, before = None):
    '''Collect comments within /r/kpop that meet various standards; returns a list of comments as json objects'''
    if before is None:
        url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=kpop&score=>{}&num_comments=>{}&size={}'.format(min_score, min_num_comments, request_size)
    else:
        url = 'https://api.pushshift.io/reddit/search/submission/?subreddit=kpop&score=>{}&num_comments=>{}&size={}&before={}'.format(min_score, min_num_comments, request_size, before)
    response = requests.get(url, headers = headers)
    return response.json()['data']

def file_exists(filename):
    return os.path.exists(filename)

def collect_comment(post_data, size_to_collect = 50, info_to_collect = ['body'], write_to_file=True):
    if post_data['num_comments'] > size_to_collect:
        logging.warning('Post {} has more than {} comments; only {} most recent comments will be collected'.format(post_data['id'], size_to_collect, size_to_collect))
    post_id = post_data['id']
    output_file = 'data/comments/{}-{}-comments.pkl'.format(post_id, size_to_collect)

    if file_exists(output_file):
        return load_data(output_file)
    
    url = 'https://api.pushshift.io/reddit/comment/search?link_id={}&size={}'.format(post_id, size_to_collect)

    response = requests.get(url, headers = headers)

    comments_json = None
    try:
        comments_json = response.json()['data']
    except Exception as e:
        print('Exception {} occurred for post {}'.format(e, post_id))

    if comments_json is None:
        return
    
    if len(info_to_collect) > 1:
        comment_data = {}
        for info in info_to_collect:
            comment_data[info] = [comment[info] for comment in comments_json]
    else:
        comment_data = [comment[info_to_collect[0]] for comment in comments_json]

    if write_to_file:
        save_data(comment_data, output_file)

    return comment_data


def save_data(item_to_save, filename, mode='wb'):
    with open(filename, mode) as f:
        pickle.dump(item_to_save, f)

def load_data(filename, mode='rb'):
    try:
        with open(filename, mode) as f:
            data = pickle.load(f)
    except:
        logging.debug('Cannot locate {}'.format(filename))
        data = None
    return data