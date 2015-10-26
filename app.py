__author__ = 'alla'
from flask import Flask, jsonify, g, request
import json
from db import init_db, get_db
from api.user import user
from api.forum import forum
from api.post import post
from api.thread import thread
from pymysql import DatabaseError


app = Flask(__name__)
BASE_URL = "/db/api"
app.register_blueprint(user, url_prefix= BASE_URL)
app.register_blueprint(forum, url_prefix= BASE_URL)
app.register_blueprint(post, url_prefix= BASE_URL)
app.register_blueprint(thread, url_prefix= BASE_URL)

get_status = "SELECT COUNT(User.id) FROM USER UNION SELECT COUNT(Forum.id) FROM Forum UNION SELECT COUNT(Thread.id) FROM Thread UNION SELECT COUNT(Post.id) FROM Post;"


@app.route(BASE_URL + '/status/')
def status():
    try:
        db = get_db()
        cursor = db.cursor()
    except DatabaseError as e:
        return json.dumps({{"code": 4, "response": "Uncnow error"}})
    try:
        cursor.execute("SELECT COUNT(User.id) FROM USER")
        user = cursor.fetchall()[0]
        cursor.execute("SELECT COUNT(Thread.id) FROM Thread")
        thread = cursor.fetchall()[0]
        cursor.execute("SELECT COUNT(Forum.id) FROM Forum")
        forum = cursor.fetchall()[0]
        cursor.execute("SELECT COUNT(Post.id) FROM Post")
        post = cursor.fetchall()[0]
    except (DatabaseError) as e:
        cursor.close()
        return json.dumps({{"code": 4, "response": "Uncnow error"}})
    return json.dumps({"code": 0, "response": {"user": user[0], "thread": thread[0], "forum": forum[0], "post": post[0]}})

@app.route(BASE_URL + '/clear/', methods=['GET','POST'])
def clear():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM followers;")
        cursor.execute("DELETE FROM subscriptions;")
        cursor.execute("DELETE FROM Post;")
        cursor.execute("DELETE FROM Thread;")
        cursor.execute("DELETE FROM Forum;")
        cursor.execute("DELETE FROM User;")
        db.commit()
    except (DatabaseError) as e:
        cursor.close()
        return json.dumps({{"code": 4, "response": "Uncnow error"}})
    cursor.close()
    return json.dumps({"code": 0, "response": "OK"})

@app.route('/')
def index():
    return 'Index Page'

if __name__ == '__main__':
    app.run("127.0.0.1", port=8080)


