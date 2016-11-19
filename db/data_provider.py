import sqlite3
import os


class DataProvider:

    _db = None
    _filename = 'posts.db'

    def __init__(self):
        base_path = os.path.dirname(__file__)
        db_path = os.path.join(base_path, self._filename)
        self._db = sqlite3.connect(db_path)

    def get_post_text(self):
        query = 'SELECT post_id, post_text FROM posts WHERE is_posted = 0 LIMIT 1'
        post = self._db.execute(query).fetchall()

        # Помечаем пост как использованый
        query = 'UPDATE posts SET is_posted = 1 WHERE post_id = {}'.format(post[0][0])
        self._db.execute(query)
        self._db.commit()
        post_text = post[0][1].replace('""', '"')
        return post_text

    def add_new_text(self, text):
        query = 'INSERT OR IGNORE INTO posts VALUES (NULL, "{}", 0)'.format(text)
        self._db.execute(query)
        self._db.commit()

    def check_posts_in_base(self):
        query = 'SELECT COUNT(*) FROM posts WHERE is_posted = 0'
        count = self._db.execute(query).fetchall()[0][0]
        if count == 0:
            return False
        else:
            return True

    def close_conn(self):
        self._db.close()
