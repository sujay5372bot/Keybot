import sqlite3, time

db = sqlite3.connect("users.db", check_same_thread=False)
cur = db.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)")
cur.execute("CREATE TABLE IF NOT EXISTS rules (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, source INTEGER, dest INTEGER, keywords TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS forwarding (user_id INTEGER PRIMARY KEY, status INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS premium (user_id INTEGER PRIMARY KEY, expiry INTEGER)")
db.commit()

def add_user(uid):
    cur.execute("INSERT OR IGNORE INTO users VALUES (?)", (uid,))
    db.commit()

def add_rule(uid, s, d, k):
    cur.execute("INSERT INTO rules (user_id, source, dest, keywords) VALUES (?,?,?,?)", (uid,s,d,k))
    db.commit()

def get_rules(uid):
    cur.execute("SELECT source, dest, keywords FROM rules WHERE user_id=?", (uid,))
    return cur.fetchall()

def start_forward(uid):
    cur.execute("INSERT OR REPLACE INTO forwarding VALUES (?,1)", (uid,))
    db.commit()

def stop_forward(uid):
    cur.execute("UPDATE forwarding SET status=0 WHERE user_id=?", (uid,))
    db.commit()

def is_forwarding(uid):
    cur.execute("SELECT status FROM forwarding WHERE user_id=?", (uid,))
    r = cur.fetchone()
    return r and r[0] == 1

def set_premium(uid, days):
    exp = int(time.time()) + days*86400
    cur.execute("INSERT OR REPLACE INTO premium VALUES (?,?)", (uid, exp))
    db.commit()

def is_premium(uid):
    cur.execute("SELECT expiry FROM premium WHERE user_id=?", (uid,))
    r = cur.fetchone()
    return r and r[0] > int(time.time())

def remove_expired():
    cur.execute("DELETE FROM premium WHERE expiry < ?", (int(time.time()),))
    db.commit()

def stats():
    return {
        "users": cur.execute("SELECT COUNT(*) FROM users").fetchone()[0],
        "premium": cur.execute("SELECT COUNT(*) FROM premium").fetchone()[0],
        "forwarding": cur.execute("SELECT COUNT(*) FROM forwarding WHERE status=1").fetchone()[0]
    }
