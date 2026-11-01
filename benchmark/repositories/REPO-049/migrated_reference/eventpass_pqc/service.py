"""SQLite pass lifecycle using ML-DSA-65 signatures."""
import sqlite3
import time
from pathlib import Path
from .crypto import canonical_pass, sign_pass, verify_pass


class EventPassPQC:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS passes(pass_id TEXT PRIMARY KEY,event_id TEXT NOT NULL,holder_alias TEXT NOT NULL,serial INTEGER NOT NULL UNIQUE,expires_at INTEGER NOT NULL,payload BLOB NOT NULL,signature BLOB NOT NULL,status TEXT NOT NULL)")

    def issue(self, pass_id: str, event_id: str, holder_alias: str, serial: int, expires_at: int, private) -> None:
        payload = canonical_pass(pass_id, event_id, holder_alias, serial, expires_at)
        signature = sign_pass(payload, private)
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO passes VALUES(?,?,?,?,?,?,?,'active')", (pass_id,event_id,holder_alias,serial,expires_at,payload,signature))

    def revoke(self, pass_id: str) -> bool:
        with sqlite3.connect(self.path) as db:
            return db.execute("UPDATE passes SET status='revoked' WHERE pass_id=? AND status='active'", (pass_id,)).rowcount == 1

    def verify_offline(self, pass_id: str, public, *, now: int | None = None, revoked_snapshot: set[str] | None = None) -> bool:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT payload,signature,expires_at,status FROM passes WHERE pass_id=?", (pass_id,)).fetchone()
        if row is None or row[3] != "active" or pass_id in (revoked_snapshot or set()):
            return False
        return (row[2] > (int(time.time()) if now is None else now)
                and verify_pass(row[0], row[1], public))

    def duplicate_serial(self, serial: int) -> bool:
        with sqlite3.connect(self.path) as db:
            return db.execute("SELECT 1 FROM passes WHERE serial=?", (serial,)).fetchone() is not None
