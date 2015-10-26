__author__ = 'alla'
from flask import request
from flask import Blueprint
from db import get_db
from pymysql import DatabaseError
from  function import *
from sql import *
from response import *


thread = Blueprint('thread', __name__)
BASE_URL = "/thread"

@thread.route(BASE_URL + '/details/')
def datails():
    id = request.args.get('thread')
    if(id == None):
        return response_2
    related_list = request.args.getlist('related')
    for related in related_list:
        if related not in ['user', 'forum']:
            return response_3
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    if(cursor.execute(get_thread_id, [id]) == 0 ):
        cursor.close()
        return response_1
    response = make_response_for_thread(id, cursor, related_list)
    cursor.close()
    return make_response(0, response)


@thread.route(BASE_URL + '/close/', methods=['GET','POST'])
def close():
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
       id = data['thread']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [id]) == 0 ):
        return response_1
    try:
        cursor.execute(close_thread,[id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})

@thread.route(BASE_URL + '/create/', methods=['GET','POST'])
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
       forum = data['forum']
       title = data['title']
       isClosed = data['isClosed']
       user = data['user']
       date = data['date']
       message  = data['message']
       slug = data['slug']
    except (KeyError):
        cursor.close()
        return response_2
    user_id = Get_user_id(user,cursor)
    forum_id = Get_forum_id(forum,cursor)
    if user_id == -1 or forum_id == -1:
        cursor.close()
        return response_1
    try:
        isDeleted = data['isDeleted']
    except (KeyError):
        isDeleted = False
    try:
        cursor.execute(create_thread, [title, date, message, slug, user_id, forum_id, isClosed, isDeleted])
        db.commit()
    except DatabaseError as e:
        return response_4
    cursor.execute(get_last_id_for_thread)
    id = cursor.fetchone()[0]
    reaponse = make_response_for_thread(id, cursor)
    cursor.close()
    return make_response(0, reaponse)


@thread.route(BASE_URL + '/list/')
def list():
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    forum = request.args.get('forum')
    user = request.args.get('user')
    if (forum == None and user == None) or (forum != None and user != None):
        return response_2
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    if forum != None:
        get_list_id = get_list_thread_by_forum_id
        id = Get_forum_id(forum, cursor)
        if id == -1:
            cursor.close()
            return response_1
    else:
        id = Get_user_id(user, cursor)
        if id == -1:
            cursor.close()
            return response_1
        get_list_id = get_list_thread_id_by_user
    try:
        cursor.execute(get_list_id + add_order + add_limit,[id, since])
        list_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list = []
    for t_id in list_id:
        post = make_response_for_thread(t_id[0], cursor, [])
        list.append(post)
    cursor.close()
    return make_response(0, list)


tree = 'SELECT id FROM Post WHERE Thread_id = %s AND date >= %s'

@thread.route(BASE_URL + '/listPosts/')
def listPosts():
    thread = request.args.get('thread')
    if(thread == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    related_list = request.args.getlist('related')
    if(cursor.execute(get_thread_id, [thread]) == 0 ):
        cursor.close()
        return response_1
    since = Optional_sience_date(request)
    add_order = Optional_order(request)
    limit = request.args.get('limit')
    if limit != None:
        add_limit = ' LIMIT '+limit+";"
    else:
        add_limit = ";"
    sort = request.args.get('sort')
    if sort == 'tree':
        try:
            add_order = Optional_order_by_mpath(request)
            cursor.execute(tree + add_order + add_limit, [thread, since])
            list_id = cursor.fetchall()
        except DatabaseError as e:
            cursor.close()
            return response_4
    elif sort == None or sort == 'flat':
        try:
            cursor.execute(list_id_post_by_thread_id +add_order + add_limit,[thread, since])
            list_id = cursor.fetchall()
        except (DatabaseError):
            cursor.close()
            return response_4
    elif sort == 'parent_tree':
        try:
            cursor.execute("SELECT id FROM Post WHERE parent IS NULL AND Post.Thread_id = %s AND date >= %s" + add_order + add_limit,[thread, since])
            list = cursor.fetchall()
            list_id = []
            for i in list:
                cursor.execute("SELECT id FROM Post WHERE mpath LIKE %s;",['/'+str(i[0])+'%'])
                a = cursor.fetchall()
                list_id.extend(a)
        except DatabaseError:
            cursor.close()
            return response_4
    list_post = []
    for post_id in list_id:
        list_post.append(make_response_for_post(post_id, cursor, related_list))
    cursor.close()
    return make_response(0, list_post)


@thread.route(BASE_URL + '/open/', methods=['GET','POST'])
def open():
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
       id = data['thread']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [id]) == 0 ):
        return response_1
    try:
        cursor.execute(open_thread,[id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})

@thread.route(BASE_URL + '/remove/', methods=['GET','POST'])
def remove():
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
       id = data['thread']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [id]) == 0 ):
        return response_1
    try:
        cursor.execute(remove_thread,[id])
        cursor.execute(remove_the_posts_in_the_thread, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})


@thread.route(BASE_URL + '/restore/', methods=['GET','POST'])
def restore():
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
       id = data['thread']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [id]) == 0 ):
        return response_1
    try:
        cursor.execute(restore_thread,[id])
        cursor.execute(restore_the_posts_in_the_thread, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    cursor.close()
    return make_response(0, {"thread": id})


@thread.route(BASE_URL + '/subscribe/', methods=['GET','POST'])
def subscribe():
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
       thread = data['thread']
       user = data['user']
    except (KeyError):
        cursor.close()
        return response_2
    user_id = Get_user_id(user, cursor)
    if user_id == -1 or (cursor.execute(get_thread_id, [thread]) == 0 ):
        cursor.close()
        return response_1
    id = Get_subscribe_id(user_id, thread, cursor)
    if id != -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(get_subscribe, [user_id, thread])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = {
        "thread": thread,
        "user": user
    }
    cursor.close()
    return make_response(0, response)



@thread.route(BASE_URL + '/unsubscribe/', methods=['GET','POST'])
def unsubscribe():
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
       thread = data['thread']
       user = data['user']
    except (KeyError):
        cursor.close()
        return response_2
    user_id = Get_user_id(user, cursor)
    if user_id == -1 or (cursor.execute(get_thread_id, [thread]) == 0 ):
        cursor.close()
        return response_1
    id = Get_subscribe_id(user_id, thread, cursor)
    if id == -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(get_unsubscribe, [id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = {
        "thread": thread,
        "user": user
    }
    cursor.close()
    return make_response(0, response)

@thread.route(BASE_URL + '/update/', methods=['GET','POST'])
def update():
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
       thread = data['thread']
       message  = data['message']
       slug = data['slug']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [thread]) == 0 ):
        return response_1
    try:
        cursor.execute(update_thread, [message, slug, thread])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_thread(thread, cursor)
    cursor.close()
    return make_response(0, response)



@thread.route(BASE_URL + '/vote/', methods=['GET','POST'])
def vote():
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
       thread_id = data['thread']
       vote = data['vote']
    except (KeyError):
        cursor.close()
        return response_2
    if(cursor.execute(get_thread_id, [thread_id]) == 0 ):
        cursor.close()
        return response_1
    if vote == 1:
        query = get_like_for_thread
    elif vote == -1:
        query = get_dislike_for_thread
    else:
        cursor.close()
        return response_2
    try:
        cursor.execute(query, [thread_id])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_thread(thread_id, cursor)
    cursor.close()
    return make_response(0, response)