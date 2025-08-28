import sqlite3
import os

DB_FOLDER = 'databases'
os.makedirs(DB_FOLDER, exist_ok=True)

def get_db_connection(country):
    country = country.lower()
    db_name_map = {
        'germany': 'vpn_keys_germany.db',
        'finland': 'vpn_keys_finland.db',
        'spb': 'vpn_keys_spb.db'
    }
    if country not in db_name_map:
        raise ValueError(f"Неизвестная страна: {country}")
    db_path = os.path.join(DB_FOLDER, db_name_map[country])
    return sqlite3.connect(db_path)

def setup_databases():
    for country in ['germany', 'finland', 'spb']:
        conn = get_db_connection(country)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vpn_keys (
                tg_id INTEGER,
                key TEXT
            )
        ''')
        conn.commit()
        conn.close()

def add_vpn_key(tg_id, country, key):
    conn = get_db_connection(country)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO vpn_keys (tg_id, key) VALUES (?, ?)', (tg_id, key))
    conn.commit()
    conn.close()

def get_vpn_key(tg_id, country):
    conn = get_db_connection(country)
    cursor = conn.cursor()
    cursor.execute('SELECT key FROM vpn_keys WHERE tg_id = ?', (tg_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

setup_databases()
