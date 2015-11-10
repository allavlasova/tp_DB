__author__ = 'alla'
from flask import request
from flask import Blueprint
from db import get_db
from pymysql import DatabaseError
from  function import *
from response import *
forum = Blueprint('forum', __name__)
BASE_URL = "/forum"


@forum.route(BASE_URL + '/create/', methods=['GET', 'POST'])
def create():
    if(request.method == 'GET'):
        return make_response(2, "no valid maethod")
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       name = data['name']
       short_name = data['short_name']
       user = data['user']
    except (KeyError):
        cursor.close()
        return response_2
    id = Get_user_id(user, cursor)
    if id == -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(create_forum, [name, short_name, id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_forum_by_short_name(short_name,cursor,[])
    cursor.close()
    return make_response(0, response)


@forum.route(BASE_URL + '/details/')
def datails():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    related = request.args.get('related')
    id = Get_forum_id(short_name, cursor)
    if id == -1:
        cursor.close()
        return response_1
    response = make_response_for_forum(id, cursor, related)
    cursor.close()
    return make_response(0, response)

@forum.route(BASE_URL + '/listPosts/')
def listPosts():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    related_list = request.args.getlist('related')
    id = Get_forum_id(short_name, cursor)
    if id == -1:
        cursor.close()
        return make_response(1, "Forum not found")
    since = Optional_sience_date(request)
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(list_id_post +add_order + add_limit,[id, since])
        list_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list_post = []
    for post_id in list_id:
        list_post.append(make_response_for_post(post_id, cursor, related_list))
    cursor.close()
    return make_response(0, list_post)


@forum.route(BASE_URL + '/listUsers/')
def listUsers():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    id = Get_forum_id(short_name, cursor)
    if id == -1:
        cursor.close()
        return response_1
    since = request.args.get('since_id')
    if since == None:
        since = 0
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(user_id_with_posts_on_this_forum + add_order + add_limit, [id, since])
        print(user_id_with_posts_on_this_forum + add_order + add_limit)
        list_id = cursor.fetchall()
    except DatabaseError:
        cursor.close()
        return response_4
    list_user = []
    for user_id in list_id:
        list_user.append(make_response_for_user(user_id[0], cursor))
    cursor.close()
    return make_response(0, list_user)

@forum.route(BASE_URL + '/listThreads/')
def listThreads():
    short_name = request.args.get('forum')
    if(short_name == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    id = Get_forum_id(short_name, cursor)
    if id == -1:
        cursor.close()
        return response_1
    related_list = request.args.getlist('related')
    since = Optional_sience_date(request)
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    try:
        cursor.execute(list_threads_id + add_order + add_limit,[id, since])
        list_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list_threads = []
    for thread_id in list_id:
        list_threads.append(make_response_for_thread(thread_id, cursor, related_list))
    cursor.close()
    return make_response(0, list_threads)
