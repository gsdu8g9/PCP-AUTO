import sqlite3
import os


class DataProvider:

    _db = None

    def __init__(self, filename):
        base_path = os.path.dirname(__file__)
        db_path = os.path.join(base_path, filename)
        self._db = sqlite3.connect(db_path)

    def get_post_text(self):
        query = 'SELECT post_id, post_text FROM posts WHERE is_posted = FALSE LIMIT 1'
        post = self._db.execute(query)
        #Помечаем пост как использованый
        query = 'UPDATE posts SET is_posted = TRUE WHERE post_id = {}'.format(post[0][0])
        return post[0][1]


DataProvider('mian.py')