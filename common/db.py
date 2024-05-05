import sqlite3


def write_to_db(email, profile_info, user_info, perspective):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
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


def read_from_db(email):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    conn.close()
    if record:
        return record[1], record[2], record[3]
