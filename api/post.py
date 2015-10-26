__author__ = 'alla'
from flask import request
from flask import Blueprint
from db import get_db
from pymysql import DatabaseError
from  function import *
from sql import *
from response import *

post = Blueprint('post', __name__)
BASE_URL = "/post"


@post.route(BASE_URL + '/details/')
def datails():
    id = request.args.get('post')
    if(id == None or id < 0):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    related = request.args.getlist('related')
    for i in related:
        if i not in ['user', 'thread', 'forum']:
            cursor.close()
            return response_3
    if(cursor.execute(get_post_id, [id]) == 0 ):
        return response_1
    response = make_response_for_post(id, cursor, related)
    cursor.close()
    return make_response(0, response)

mpath = 'UPDATE Post SET `mpath`=%s WHERE id=%s;'
get_mpath = 'SELECT mpath FROM Post WHERE id = %s'

@post.route(BASE_URL + '/create/', methods=['GET','POST'])
def create():
    if(request.method == 'GET'):
        return response_2
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
       date = data['date']
       thread = data['thread']
       message = data['message']
       user = data['user']
       forum = data['forum']
    except (KeyError):
        cursor.close()
        return response_2
    user_id = Get_user_id(user,cursor)
    if user_id == -1:
        cursor.close()
        return response_1
    forum_id = Get_forum_id(forum,cursor)
    if forum_id == -1:
        cursor.close()
        return response_1
    if(cursor.execute(get_thread_id, [thread]) == 0 ):
        cursor.close()
        return response_1
    parametr = []
    parametr.append(date)
    parametr.append(thread)
    parametr.append(message)
    parametr.append(user_id)
    parametr.append(forum_id)
    try:
        parent = data['parent']
        if(cursor.execute(get_post_id, [parent]) == 0):
            cursor.close()
            return response_1
    except KeyError:
        parent = None
    try:
        isApproved = data['isApproved']
    except KeyError:
        isApproved = False
    try:
        isHighlighted = data['isHighlighted']
    except KeyError:
        isHighlighted = False
    try:
        isEdited = data['isEdited']
    except KeyError:
        isEdited = False
    try:
        isSpam = data['isSpam']
    except KeyError:
        isSpam = False
    try:
        isDeleted = data['isDeleted']
    except KeyError:
        isDeleted = False
    parametr.append(parent)
    parametr.append(isApproved)
    parametr.append(isHighlighted)
    parametr.append(isEdited)
    parametr.append(isSpam)
    parametr.append(isDeleted)
    try:
        cursor.execute(create_post, parametr)
        cursor.execute(get_last)
        id_post = cursor.fetchone()[0]
        if parent == None:
            cursor.execute(mpath, ['/' + str(id_post), id_post])
        else:
            cursor.execute(get_mpath, [parent])
            path = cursor.fetchone()[0]
            cursor.execute(mpath, [path + '/' + str(id_post), id_post])
        db.commit()
    except DatabaseError:
        return response_5
    cursor.execute(get_last)
    id_post = cursor.fetchone()[0]
    cursor.execute(post_data, [id_post])
    response = make_response_for_post(id_post, cursor, [])
    cursor.close()
    return make_response(0, response)

@post.route(BASE_URL + '/list/')
def list():
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    forum = request.args.get('forum')
    thread = request.args.get('thread')
    if (forum == None and thread == None) or (forum != None and thread != None):
        return response_2
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    if forum != None:
        get_list_post_id = get_list_post_by_forum_id
        id = Get_forum_id(forum,cursor)
        if id == -1:
            cursor.close()
            return response_1
    else:
        id = thread
        if(cursor.execute(get_thread_id, [id]) == 0 ):
            cursor.close()
            return response_1
        get_list_post_id = get_list_post_id_by_thread
    try:
        cursor.execute(get_list_post_id + add_order + add_limit,[id, since])
        post_list_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    post_list = []
    for post_id in post_list_id:
        post = make_response_for_post(post_id, cursor, [])
        post_list.append(post)
    cursor.close()
    return make_response(0, post_list)


@post.route(BASE_URL + '/remove/', methods=['GET','POST'])
def remove():
    if(request.method == 'GET'):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_post_id, [post_id]) == 0 ):
        return response_1
    cursor.execute("SELECT isDeleted FROM Post WHERE id = %s",[post_id])
    isDelete = cursor.fetchone()[0]
    if isDelete == 1:
        return response_2
    try:
        cursor.execute(remove_post,[post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"post": post_id})

@post.route(BASE_URL + '/restore/', methods=['GET','POST'])
def restore():
    if(request.method == 'GET'):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
    except (KeyError):
        cursor.close()
        return response_2
    cursor.execute("SELECT isDeleted FROM Post WHERE id = %s",[post_id])
    isDelete = cursor.fetchone()[0]
    if isDelete == 0:
        return response_2
    if(cursor.execute(get_post_id, [post_id]) == 0 ):
        return response_1
    try:
        cursor.execute(restore_post,[post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"post": post_id})


@post.route(BASE_URL + '/update/', methods=['GET','POST'])
def update():
    if(request.method == 'GET'):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
       message = data['message']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_post_id, [post_id]) == 0 ):
        return response_1
    try:
        cursor.execute(update_post,[message, post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_a_response_for_post(post_id, cursor)
    cursor.close()
    return make_response(0, response)

@post.route(BASE_URL + '/vote/', methods=['GET','POST'])
def vote():
    if(request.method == 'GET'):
        return response_2
    db = get_db()
    cursor = db.cursor()
    try:
        data = request.get_json()
    except ValueError:
        cursor.close()
        return response_2
    try:
       post_id = data['post']
       vote = data['vote']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_post_id, [post_id]) == 0 ):
        cursor.close()
        return response_1
    if vote == 1:
        query = get_like
    elif vote == -1:
        query = get_dislike
    else:
        cursor.close()
        return response_2
    try:
        cursor.execute(query, [post_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_a_response_for_post(post_id, cursor)
    cursor.close()
    return make_response(0, response)