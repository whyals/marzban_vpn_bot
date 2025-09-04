import sqlite3
import os

DB_FOLDER = 'marzban_vpn_bot/databases'
os.makedirs(DB_FOLDER, exist_ok=True)

DB_PATH = os.path.join(DB_FOLDER, 'test_users.db')

users_conn = sqlite3.connect(DB_PATH)
users_cursor = users_conn.cursor()

users_cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        tg_id INTEGER PRIMARY KEY,
        tg_tag TEXT,
        name TEXT,
        access_level TEXT
    )
''')
users_conn.commit()


async def add_user(tg_id, tg_tag, name, access_level):
    users_cursor.execute(
        'REPLACE INTO users (tg_id, tg_tag, name, access_level) VALUES (?, ?, ?, ?)',
        (tg_id, tg_tag, name, access_level)
    )
    users_conn.commit()


async def get_user(tg_id):
    cursor = users_conn.cursor()
    cursor.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,))
    return cursor.fetchone()


async def get_all_users():
    users_cursor.execute('SELECT tg_id, tg_tag, name FROM users')
    return users_cursor.fetchall()


async def update_user_access(tg_id, access_level):
    users_cursor.execute('UPDATE users SET access_level = ? WHERE tg_id = ?', (access_level, tg_id))
    users_conn.commit()


async def delete_user(tg_id):
    users_cursor.execute('DELETE FROM users WHERE tg_id = ?', (tg_id,))
    users_conn.commit()


async def close_users_db_connection():
    users_conn.close()


