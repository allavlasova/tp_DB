__author__ = 'alla'
import json
from sql import *
from flask import request
from pymysql import DatabaseError

def make_response(code, response):
    return json.dumps({
        "code":code,
        "response": response
    })

def user_following(id, cursor):
    cursor.execute(get_followeing,[id])
    following  = cursor.fetchall()
    result = [following[i][0] for i in range(len(following))]
    return result

def user_followers(id, cursor):
    cursor.execute(get_followers,[id])
    followers  = cursor.fetchall()
    result = [followers[i][0] for i in range(len(followers))]
    return result

def user_subscriptions(id, cursor):
    q = cursor.execute(get_subscriptions,[id])
    if q == 0:
        subscriptions = []
    else:
        subscriptions  = cursor.fetchall()
    result = [subscriptions[i][0] for i in range(len(subscriptions))]
    return result

def make_response_for_user(id, cursor):
    cursor.execute(get_user_by_id, [id])
    data = cursor.fetchall()[0]
    followers = user_followers(id, cursor)
    following = user_following(id, cursor)
    subscriptions = user_subscriptions(id, cursor)
    return {
        "about": data[2],
        "email": data[5],
        "followers": followers,
        "following": following,
        "id": id,
        "isAnonymous": data[3],
        "name": data[0],
        "subscriptions": subscriptions,
        "username": data[1]
    }


def make_a_response_for_post(id, cursor):
    cursor.execute(post_data, [id])
    data = cursor.fetchall()[0]
    return {
        "id" : id,
        "date":str(data[1]),
        "message": data[2],
        "isApporved" : data[3],
        "isDeleted" : data[4],
        "isEdited" : data[5],
        "isHighlighted": data[6],
        "isSpam" : data[7],
        "dislikes": data[8],
        "likes": data[9],
        "points": data[9] - data[8],
        "thread": data[10],
        "parent": data[11],
        "user" : data[12],
        "forum" : data[13]
    }

def make_response_for_post(id, cursor, related):
    cursor.execute(post_data, [id])
    data = cursor.fetchall()[0]
    if 'user' in related:
        user = make_response_for_user(data[14], cursor)
    else:
        user = data[12]
    if 'forum' in related:
        forum = make_response_for_forum(data[15], cursor, [])
    else:
        forum = data[13]
    if 'thread' in related:
        thread = make_response_for_thread(data[10], cursor)
    else:
        thread = data[10]
    return {
        "id" : data[0],
        "date":str(data[1]),
        "message": data[2],
        "isApproved" : data[3],
        "isDeleted" : data[4],
        "isEdited" : data[5],
        "isHighlighted": data[6],
        "isSpam" : data[7],
        "dislikes": data[8],
        "likes": data[9],
        "points": data[9] - data[8],
        "thread": thread,
        "parent": data[11],
        "user" : user,
        "forum" : forum
    }

def Get_user_id(email, cursor):
    if(cursor.execute(get_user_id, [email,]) == 0 ):
        return -1
    id = cursor.fetchone()[0]
    return id

def Get_forum_id(short_name, cursor):
    if(cursor.execute(get_forum_id, [short_name]) == 0 ):
        return -1
    id = cursor.fetchone()[0]
    return id

def make_a_response_for_user(data, followers, following, subscriptions):
    return {
        "about": data[2],
        "email": data[5],
        "followers": followers,
        "following": following,
        "id": data[4],
        "isAnonymous": data[3],
        "name": data[0],
        "subscriptions": subscriptions,
        "username": data[1]
    }



def make_a_response_for_thread(id, cursor):
    cursor.execute(data_thread, [id])
    data = cursor.fetchall()[0]
    return {
        "date": str(data[3]),
        "dislikes": data[8],
        "forum": data[10],
        "id": data[0],
        "isClosed": data[2],
        "isDeleted": data[6],
        "likes": data[7],
        "message": data[4],
        "points": 0,
        "posts": "",
        "slug": data[5],
        "title": data[1],
        "user": data[9]
    }


def make_response_for_thread(id, cursor, related = []):
    cursor.execute(data_thread, [id])
    data = cursor.fetchall()[0]
    if 'user' in related:
        user = make_response_for_user(data[12], cursor)
    else:
        user = data[9]
    if 'forum' in related:
        forum = make_response_for_forum(data[13], cursor, [])
    else:
        forum = data[10]
    return {
        "id": data[0],
        "title": data[1],
        "isClosed": data[2],
        "date": str(data[3]),
        "message": data[4],
        "slug": data[5],
        "isDeleted": data[6],
        "likes": data[7],
        "dislikes": data[8],
        "forum": forum,
        "points": int(data[7]) - int(data[8]),
        "posts": data[14],
        "user": user
    }

def Optional_order(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY date DESC'
    elif order == 'asc':
        return  ' ORDER BY date ASC'
    else:
        return ""

def optional_Order(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' DESC'
    elif order == 'asc':
        return  ' ASC'
    else:
        return ""

def Optional_order_by_id(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY id DESC'
    elif order == 'asc':
        return  ' ORDER BY id ASC'
    else:
        return ""

def Optional_order_by_mpath(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY mpath DESC'
    elif order == 'asc':
        return  ' ORDER BY mpath ASC'
    else:
        return ""

def Optional_order_by_name(request):
    order = request.args.get('order')
    if order == None or order == 'desc':
        return ' ORDER BY User.name DESC'
    elif order == 'asc':
        return  ' ORDER BY User.name ASC'
    else:
        return ""


def tree(a, query, thread, since, cursor, array, lim):
    q = cursor.execute(query, [since, a, thread])
    if q == 0 or (len(array) == lim):
        return
    else:
        a = cursor.fetchall()
        for i in a:
            if len(array) == lim:
                return
            array.append(i[0])
            tree(i[0], query, thread, since, cursor, array, lim)
    return

def tree1(a, query, thread, since, cursor, array):
    q = cursor.execute(query, [since, a, thread])
    if q == 0:
        return
    else:
        a = cursor.fetchall()
        for i in a:
            array.append(i[0])
            tree1(i[0], query, thread, since, cursor, array)
    return

def Optional_sort(request, cursor, array):
    sort = request.args.get('sort')
    if sort not in ('flat', 'tree', 'parent_tree'):
        return -1
    elif sort == 'flat':
        return 1
    elif sort == 'tree':
        tree(0, cursor, array)
        return array
    return 1

def optional_Limit(request):
    limit = request.args.get('limit')
    if limit != None:
        return ' LIMIT '+limit+";"
    else:
        return ";"


def Optional_sience_date(request):
    since = request.args.get('since')
    if since != None:
        return since
    else:
        return '0000-00-00'

def Optional_sience_id(request):
    since = request.args.get('since')
    if since != None:
        return since
    else:
        return 0


def Get_forum_id(short_name, cursor):
    if(cursor.execute(get_forum_id, [short_name]) == 0 ):
        cursor.close()
        return -1
    id = cursor.fetchone()[0]
    return id

def make_response_for_forum(id, cursor, related):
    cursor.execute(data_forum_by_id, [id])
    data = cursor.fetchall()[0]
    if related == 'user':
        user = make_response_for_user(data[3], cursor)
    else:
        user = data[4]
    return {
        "id": data[0],
        "name": data[1],
        "short_name": data[2],
        "user": user
        }

def make_response_for_forum_by_short_name(short_name, cursor, related):
    cursor.execute(data_forum, [short_name])
    data = cursor.fetchall()[0]
    if related == 'user':
        user = make_response_for_user(data[3], cursor)
    else:
        user = data[4]
    return {
        "id": data[0],
        "name": data[1],
        "short_name": data[2],
        "user": user
        }

def Get_subscribe_id(id1, id2, cursor):
    if(cursor.execute(data_subscribe, [id1,id2]) == 0):
        return -1
    id  = cursor.fetchone()[0]
    return id

def Get_user_follower_followee(id1, id2, cursor):
    if(cursor.execute(get_id_unfollow, [id1,id2]) == 0):
        return -1
    id  = cursor.fetchone()[0]
    return id

def Get_id_follower_followee(email_follower, email_followee, cursor):
    if(cursor.execute(get_id_follower_followee, [email_follower, email_followee]) == 0 ):
        return [-1,-1]
    id = cursor.fetchall()[0]
    return id
