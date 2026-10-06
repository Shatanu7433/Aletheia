import json
import os
import sqlite3
import time

DB = os.getenv("SQLITE_PATH", "research.db")  # TODO: move to Postgres + pgvector


def _conn():
    c = sqlite3.connect(DB)
    c.execute(
        "CREATE TABLE IF NOT EXISTS research (id TEXT PRIMARY KEY, question TEXT, "
        "status TEXT, created_at REAL, data TEXT)"
    )
    return c


def create(id_: str, question: str):
    with _conn() as c:
        c.execute("INSERT INTO research VALUES (?,?,?,?,?)",
                  (id_, question, "running", time.time(), "{}"))


def finish(id_: str, status: str, data: dict):
    with _conn() as c:
        c.execute("UPDATE research SET status=?, data=? WHERE id=?",
                  (status, json.dumps(data), id_))


def get(id_: str):
    with _conn() as c:
        r = c.execute("SELECT id,question,status,created_at,data FROM research WHERE id=?",
                      (id_,)).fetchone()
    if not r:
        return None
    return {"id": r[0], "question": r[1], "status": r[2], "created_at": r[3],
            **json.loads(r[4] or "{}")}


def list_all():
    with _conn() as c:
        rows = c.execute("SELECT id,question,status,created_at FROM research "
                         "ORDER BY created_at DESC LIMIT 30").fetchall()
    return [{"id": r[0], "question": r[1], "status": r[2], "created_at": r[3]} for r in rows]
