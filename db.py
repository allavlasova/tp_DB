__author__ = 'alla'
from flask import Flask,g
import pymysql
import pymysql.cursors

app = Flask(__name__)

def connect_db():
    connsect = pymysql.connect(host='localhost',
                       user='root',
                       passwd='192168215',
                       db='TP',
                       charset='utf8')
    return connsect

def get_db():
    if not hasattr(g, 'mysql_db'):
        g.mysql_db = connect_db()
    return g.mysql_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'mysql_db'):
        g.mysql_db.close()

def init_db():
    with app.app_context():
        db = get_db()
        #with app.open_resource('schema.sql', mode='r') as f:
        with open("schema.sql", "r") as f:
            db.cursor().execute(f.read())
        db.commit()

