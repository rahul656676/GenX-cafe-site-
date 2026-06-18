from flask import g, current_app
import MySQLdb
import MySQLdb.cursors


def get_db():
    if 'db' not in g:
        cfg = current_app.config

        g.db = MySQLdb.connect(
            host=cfg['MYSQL_HOST'],
            user=cfg['MYSQL_USER'],
            passwd=cfg['MYSQL_PASSWORD'],
            db=cfg['MYSQL_DB'],
            charset='utf8mb4',
            cursorclass=MySQLdb.cursors.DictCursor
        )

    return g.db


def query(sql, args=(), one=False, commit=False):
    db = get_db()

    cur = db.cursor()

    cur.execute(sql, args)

    if commit:
        db.commit()
        return cur.lastrowid

    rv = cur.fetchone() if one else cur.fetchall()

    cur.close()

    return rv


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()