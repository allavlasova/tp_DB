__author__ = 'alla'

get_user_by_email = "SELECT name, username, about, isAnonymous, id FROM User WHERE email = %s;"

get_followeing = "SELECT email FROM User INNER JOIN followers ON User.id = User_id2 WHERE User_id1 = %s"

get_followeing_id = "SELECT User_id2 FROM followers WHERE User_id1 = %s AND User_id2 >= %s ORDER BY id"

get_followers = "SELECT email FROM User INNER JOIN followers ON User.id = User_id1 WHERE User_id2 = %s;"

get_followers_id1 = "SELECT User_id1 FROM followers WHERE User_id2 = %s;"

get_followers_id = "SELECT User_id1 FROM followers WHERE User_id2 = %s AND User_id1 >= %s ORDER BY id"

get_followers_id_limit = " LIMIT %s;"

get_subscriptions = '''SELECT Thread_id FROM subscriptions INNER JOIN User ON User.id = subscriptions.User_id WHERE User.id = %s'''

get_user_id = "SELECT id FROM User WHERE email = %s;"

get_user_by_id = "SELECT name, username, about, isAnonymous, id, email FROM User WHERE id = %s;"

create_user = "INSERT INTO User (username, about, name, email, isAnonymous) VALUES (%s, %s, %s, %s, %s);"

set_follow = "INSERT INTO followers (User_id1, User_id2) VALUES (%s, %s)"

set_unfollow = "DELETE FROM followers WHERE `id`= %s;"

get_id_unfollow = "SELECT id FROM followers WHERE User_id1 = %s AND User_id2 = %s;"

update_profule = "UPDATE User SET about=%s, `name`=%s WHERE `id`=%s;"

create_forum = "INSERT INTO Forum (name, short_name, User_id) VALUES (%s, %s, %s);"

data_forum = '''SELECT Forum.id, Forum.name, Forum.short_name, Forum.User_id, User.email
                FROM Forum INNER JOIN User ON Forum.User_id = User.id WHERE Forum.short_name = %s;'''

data_forum_by_id = "SELECT Forum.id, Forum.name, Forum.short_name, Forum.User_id, User.email FROM Forum INNER JOIN User ON Forum.User_id = User.id WHERE Forum.id = %s;"

#post_data = "SELECT  id, date, message, isApporved, isDeleted, isEdited, isHighlighted, isSpam, dislikes, likes, Forum_id, User_id, Thread_id, parent FROM Post WHERE id = %s;"

post_data = '''SELECT  Post.id, date, message, isApporved, isDeleted,
                        isEdited, isHighlighted, isSpam, dislikes, likes,
                        Post.Thread_id, parent, User.email, Forum.short_name,
                        Post.User_id, Post.Forum_id FROM Post
                        INNER JOIN
                        User ON User.id = Post.User_id
                        INNER JOIN Forum ON Forum.id = Post.Forum_id WHERE Post.id = %s;'''

get_user_posts_id = "SELECT  id FROM Post WHERE User_id = %s AND date >= %s ORDER BY id"

get_forum_id = "SELECT id FROM Forum WHERE short_name = %s;"

get_post_id = "SELECT id FROM Post WHERE id = %s;"

get_thread_id = "SELECT id FROM Thread WHERE id = %s;"

get_last = "SELECT MAX(id) FROM Post"

get_last_id_for_thread = "SELECT MAX(id) FROM Thread"

get_forum = "SELECT short_name FROM Forum WHERE id = %s"

create_post = '''INSERT INTO Post (date, Thread_id, message, User_id, Forum_id, parent, isApporved, isHighlighted, isEdited, isSpam, isDeleted)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

list_post_id = "SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.id = %s;"

list_id_post = "SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.id = %s AND date >= %s ORDER BY date"

list_id_post_by_thread_id = "SELECT Post.id FROM Post WHERE Thread_id = %s AND date >= %s"

data_thread = '''SELECT Thread.id, Thread.title, Thread.isClosed, Thread.date,
                        Thread.message, Thread.slug, Thread.isDeleted, Thread.likes,
                        Thread.dislikes, User.email, Forum.short_name,
                        Thread.id, Thread.User_id, Thread.Forum_id, COUNT(Post.id) FROM Thread
                        INNER JOIN Forum ON Forum.id = Thread.Forum_id
                        INNER JOIN User ON Thread.User_id = User.id
                        INNER JOIN Post ON Post.Thread_id = Thread.id
                        WHERE Thread.id = %s AND Post.isDeleted != 1;'''

get_list_post_id_by_forum_short_name = 'SELECT Post.id FROM Forum INNER JOIN Post ON Post.Forum_id = Forum.id WHERE Forum.short_name = %s;'

get_list_post_id_by_thread = "SELECT Post.id FROM Post WHERE Post.Thread_id = %s  AND date >= %s"

get_list_post_by_forum_id = "SELECT Post.id FROM Post WHERE Post.Forum_id = %s  AND date >= %s"

get_list_thread_by_forum_id = "SELECT Thread.id FROM Thread WHERE Thread.Forum_id = %s  AND date >= %s"

get_list_thread_id_by_user = "SELECT Thread.id FROM Thread WHERE Thread.User_id = %s  AND date >= %s"

remove_post = "UPDATE Post SET isDeleted = 1 WHERE id = %s;"

restore_post = "UPDATE Post SET isDeleted = 0 WHERE id = %s;"

update_post = "UPDATE Post SET message = %s WHERE id =  %s;"

get_like = "UPDATE Post SET likes=likes+1 WHERE id=%s;"

get_dislike = "UPDATE Post SET dislikes = dislikes + 1 WHERE id=%s;"

get_like_for_thread = "UPDATE Thread SET likes=likes+1 WHERE id=%s;"

get_dislike_for_thread = "UPDATE Thread SET dislikes = dislikes + 1 WHERE id=%s;"

user_id_with_posts_on_this_forum = "SELECT DISTINCT Post.User_id FROM Post INNER JOIN User ON User.id = Post.User_id WHERE Forum_id = %s AND User_id>= %s ORDER BY name"

list_threads_id = "SELECT id FROM Thread WHERE Forum_id = %s AND date >= %s ORDER BY date"

close_thread = "UPDATE Thread  SET  isClosed ='1' WHERE `id`= %s;"

open_thread = "UPDATE Thread  SET  isClosed ='0' WHERE `id`= %s;"

remove_thread = "UPDATE Thread  SET  isDeleted = True WHERE `id`= %s;"

restore_thread = "UPDATE Thread  SET  isDeleted = False WHERE `id`= %s;"

create_thread = "INSERT INTO Thread (title, date, message, slug, User_id, Forum_id, isClosed, isDeleted) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"


get_subscribe = "INSERT INTO subscriptions (`User_id`, `Thread_id`) VALUES (%s, %s);"

data_subscribe = "SELECT subscriptions.id FROM subscriptions WHERE User_id = %s AND Thread_id = %s;"

get_unsubscribe = "DELETE FROM subscriptions WHERE id = %s ;"

update_thread = "UPDATE Thread SET message= %s, slug = %s WHERE id = %s;"


get_isDelete = "SELECT isDeleted FROM Post WHERE id = %s"


get_id_follower_followee = '''SELECT u1.id, u2.id FROM USER AS u1
JOIN
USER AS u2 WHERE u1.email = %s AND u2.email=%s;'''

remove_the_posts_in_the_thread = "UPDATE Post SET `isDeleted`='1' WHERE Thread_id= %s;"

restore_the_posts_in_the_thread = "UPDATE Post SET `isDeleted`='0' WHERE Thread_id= %s;"