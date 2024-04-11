from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sqlite3

app = FastAPI()


def read_from_db(email):
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_info (email text, profile_info text, user_info text, perspective text)")
    c.execute("SELECT * FROM user_info WHERE email=?", (email,))
    record = c.fetchone()
    conn.close()
    print(record)
    if record is not None:
        return record[1], record[2], record[3]
    else:
        return email, "N/A", "N/A"

@app.get("/api/perspective/{email}")
def perspective(email: str):
    print(email)
    _, _, perspective = read_from_db(email)
    return perspective

