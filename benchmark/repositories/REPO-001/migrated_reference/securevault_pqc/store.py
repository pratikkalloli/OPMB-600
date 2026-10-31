"""Reference-version SQLite persistence for encrypted SecureVault objects."""
from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class SealedObject:
    object_id: str
    filename: str
    nonce: bytes
    ciphertext: bytes
    wrapped_key: bytes
    signature: bytes

class VaultStore:
    """Small local store that persists ciphertext and cryptographic metadata only."""
    def __init__(self, database: str | Path) -> None:
        self.database = str(database)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS objects (object_id TEXT PRIMARY KEY, filename TEXT NOT NULL, nonce BLOB NOT NULL, ciphertext BLOB NOT NULL, wrapped_key BLOB NOT NULL, signature BLOB NOT NULL)")

    def put(self, item: SealedObject) -> None:
        with self._connect() as db:
            db.execute("INSERT INTO objects VALUES (?, ?, ?, ?, ?, ?)", (item.object_id,item.filename,item.nonce,item.ciphertext,item.wrapped_key,item.signature))

    def get(self, object_id: str) -> SealedObject | None:
        with self._connect() as db:
            row=db.execute("SELECT * FROM objects WHERE object_id=?", (object_id,)).fetchone()
        return SealedObject(**dict(row)) if row else None

    def delete(self, object_id: str) -> bool:
        with self._connect() as db:
            cursor=db.execute("DELETE FROM objects WHERE object_id=?", (object_id,))
        return cursor.rowcount == 1
