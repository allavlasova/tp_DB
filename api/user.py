__author__ = 'alla'
from flask import Flask, request
from flask import Blueprint
import json
from db import get_db
from function import *
from pymysql import DatabaseError
from sql import *
from response import *

user = Blueprint('user', __name__)
BASE_URL = "/user"

@user.route(BASE_URL + '/details/')
def datails():
    db = get_db()
    cursor = db.cursor()
    email = request.args.get('user')
    if(email == None):
        return make_response(2, error_2)
    id = Get_user_id(email, cursor)
    if id == -1:
        cursor.close()
        return response_1
    response = make_response_for_user(id, cursor)
    cursor.close()
    return make_response(0, response)

@user.route(BASE_URL + '/create/', methods=['GET','POST'])
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
        email = data['email']
        username = data['username']
        name = data['name']
        about = data['about']
    except (KeyError):
        cursor.close()
        return response_2
    try:
        isAnonymous = data['isAnonymous']
    except (KeyError):
        isAnonymous = False
    try:
        cursor.execute(create_user,[username, about, name, email, isAnonymous])
        db.commit()
    except (DatabaseError):
        return  response_5
    id = Get_user_id(email, cursor)
    if id == -1:
        cursor.close()
        return response_1
    responce = {
        "about": about,
        "email": email,
        "id": id,
        "isAnonymous": isAnonymous,
        "name": name,
        "username": username
    }
    cursor.close()
    return make_response(0, responce)


@user.route(BASE_URL + '/follow/', methods=['GET','POST'])
def follow():
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
        follower = data['follower']
        followee = data['followee']
    except (KeyError):
        cursor.close()
        return response_2
    id_follower_followee = Get_id_follower_followee(follower, followee, cursor)
    if -1 in id_follower_followee:
        cursor.close()
        return response_1
    id = Get_user_follower_followee(id_follower_followee[0], id_follower_followee[1], cursor)
    if id != -1:
        return response_1
    try:
        cursor.execute(set_follow, [id_follower_followee[0], id_follower_followee[1]])
        db.commit()
    except DatabaseError:
        cursor.close()
        return response_4
    response = make_response_for_user(id_follower_followee[0], cursor)
    cursor.close()
    return make_response(0, response)

@user.route(BASE_URL + '/unfollow/', methods=['GET','POST'])
def unfollow():
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
        follower = data['follower']
        followee = data['followee']
    except (KeyError):
        cursor.close()
        return response_2
    id_follower_followee = Get_id_follower_followee(follower, followee, cursor)
    if -1 in id_follower_followee:
        cursor.close()
        return response_1
    id = Get_user_follower_followee(id_follower_followee[0], id_follower_followee[1], cursor)
    if id == -1:
        return response_1
    try:
        cursor.execute(set_unfollow,[id, ])
        db.commit()
    except (DatabaseError):
        cursor.close()
        return response_4
    response = make_response_for_user(id_follower_followee[0], cursor)
    cursor.close()
    return make_response(0, response)

@user.route(BASE_URL + '/listFollowers/')
def listFollowers():
    email = request.args.get('user')
    if(email == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    id = Get_user_id(email, cursor)
    if id == -1:
        cursor.close()
        return response_1
    since = Optional_sience_id(request)
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    try:
        cursor.execute(get_followers_id + add_order + add_limit,[id, since])
        followers_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list_followers = []
    for follower_id in followers_id:
        user = make_response_for_user(follower_id[0], cursor)
        list_followers.append(user)
    cursor.close()
    return make_response(0, list_followers)

@user.route(BASE_URL + '/listFollowing/')
def listFollowing():
    email = request.args.get('user')
    if(email == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    id = Get_user_id(email,cursor)
    if id == -1:
        cursor.close()
        return response_1
    since = Optional_sience_id(request)
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    try:
        cursor.execute(get_followeing_id + add_order + add_limit,[id, since])
        followeing_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list_following = []
    for followee_id in followeing_id:
        response = make_response_for_user(followee_id[0], cursor)
        list_following.append(response)
    return make_response(0, list_following)


@user.route(BASE_URL + '/listPosts/')
def listPosts():
    email = request.args.get('user')
    if(email == None):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    id = Get_user_id(email,cursor)
    if id == -1:
        cursor.close()
        return response_1
    since = Optional_sience_id(request)
    add_order = optional_Order(request)
    add_limit = optional_Limit(request)
    if add_order == "":
        cursor.close()
        return response_2
    try:
        cursor.execute(get_user_posts_id + add_order + add_limit,[id, since])
        posts_id = cursor.fetchall()
    except (DatabaseError):
        cursor.close()
        return response_4
    list_posts = []
    for post_id in posts_id:
        list_posts.append(make_response_for_post(post_id[0], cursor, []))
    return make_response(0, list_posts)


@user.route(BASE_URL + '/updateProfile/', methods=['GET','POST'])
def updateProfile():
    if(request.method == 'GET'):
        return response_2
    try:
        db = get_db()
    except DatabaseError:
        return response_4
    cursor = db.cursor()
    data = request.get_json()
    try:
        email = data['user']
        name = data['name']
        about = data['about']
    except (KeyError):
        cursor.close()
        return response_2
    id = Get_user_id(email, cursor)
    if id == -1:
        cursor.close()
        return response_1
    try:
        cursor.execute(update_profule, [about, name, id])
        db.commit()
    except (DatabaseError):
        return  response_4
    response = make_response_for_user(id, cursor)
    cursor.close()
    return make_response(0, response)


