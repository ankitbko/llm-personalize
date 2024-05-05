import sqlite3
from typing import List


def create_userinfo_table():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
    conn.commit()
    conn.close()


def create_user_additional_info_table():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute(
        'CREATE TABLE IF NOT EXISTS user_additional_info (email text, email_body text)')
    conn.commit()
    conn.close()


def write_to_user_additional_info(email: str, email_bodies: List[str]):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_user_additional_info_table()
    for body in email_bodies:
        c.execute("INSERT INTO user_additional_info VALUES (?,?)",
                  (email, str(body)))
    conn.commit()
    conn.close()


def read_from_user_additional_info(email: str):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_user_additional_info_table()
    c.execute("SELECT * FROM user_additional_info WHERE email=?", (email,))
    records = c.fetchall()
    conn.close()
    return records


def delete_from_user_additional_info(email: str):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_user_additional_info_table()
    c.execute("DELETE FROM user_additional_info WHERE email=?", (email,))
    conn.commit()
    conn.close()


def write_to_userinfo(email, profile_info, user_info, perspective):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_userinfo_table()
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    if record:
        c.execute("UPDATE user_info SET profile_info=?, user_info=?, perspective=? WHERE email=?",
                  (profile_info, user_info, perspective, email))
    else:
        c.execute("INSERT INTO user_info VALUES (?,?,?,?)",
                  (email, profile_info, user_info, perspective))
    conn.commit()
    conn.close()


def read_from_userinfo(email):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_userinfo_table()
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    conn.close()
    if record:
        return record[1], record[2], record[3]


def delete_from_userinfo(email):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    create_userinfo_table()
    c.execute("DELETE FROM user_info WHERE email=?", (email,))
    conn.commit()
    conn.close()
