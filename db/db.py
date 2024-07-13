import sqlite3, os.path

DB_PATH = './data/database.db'
BUILD_PATH = './data/build.sql'

con = sqlite3.connect(DB_PATH, check_same_thread=False)
cur = con.cursor()

def with_commit(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        commit()
        return result
    return inner

@with_commit
def build():
    if os.path.isfile(BUILD_PATH):
        scriptexec(BUILD_PATH)

def commit():
    con.commit()

def close():
    con.close()

def field(command, *values):
    cur.execute(command, values)
    fetch = cur.fetchone()
    return fetch[0] if fetch else None

def record(command, *values):
    cur.execute(command, values)
    return cur.fetchone()

def column(command, *values):
    cur.execute(command, values)
    return [item[0] for item in cur.fetchall()]

@with_commit
def execute(command, *values):
    cur.execute(command, values)
    return cur.rowcount

@with_commit
def scriptexec(path):
    with open(path, 'r', encoding='utf-8') as script:
        cur.executescript(script.read())