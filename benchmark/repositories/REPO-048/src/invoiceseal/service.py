"""Persistent invoice issue, revision, signing and verification workflow."""
from __future__ import annotations

import sqlite3
import time
from pathlib import Path

from .crypto import canonical_invoice, invoice_digest, sign_invoice, verify_invoice, signature_id


class InvoiceSeal:
    def __init__(self, path: str | Path):
        self.path = str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS invoices(invoice_id TEXT PRIMARY KEY, issuer TEXT NOT NULL, amount_minor INTEGER NOT NULL, currency TEXT NOT NULL, revision INTEGER NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS signatures(signature_id TEXT PRIMARY KEY, invoice_id TEXT NOT NULL, issuer TEXT NOT NULL, revision INTEGER NOT NULL, algorithm TEXT NOT NULL, payload_digest TEXT NOT NULL, payload BLOB NOT NULL, signature BLOB NOT NULL, created INTEGER NOT NULL)")

    def issue(self, invoice_id: str, issuer: str, amount_minor: int, currency: str) -> None:
        canonical_invoice(invoice_id, issuer, amount_minor, currency, 1)
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO invoices VALUES(?,?,?,?,1)", (invoice_id, issuer, amount_minor, currency.upper()))

    def revise_amount(self, invoice_id: str, amount_minor: int) -> int:
        if amount_minor < 0:
            raise ValueError("amount must be nonnegative")
        with sqlite3.connect(self.path) as db:
            result = db.execute("UPDATE invoices SET amount_minor=?, revision=revision+1 WHERE invoice_id=?", (amount_minor, invoice_id))
            if result.rowcount != 1:
                raise KeyError("invoice not found")
            return db.execute("SELECT revision FROM invoices WHERE invoice_id=?", (invoice_id,)).fetchone()[0]

    def sign_current(self, invoice_id: str, private) -> str:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT issuer, amount_minor, currency, revision FROM invoices WHERE invoice_id=?", (invoice_id,)).fetchone()
        if row is None:
            raise KeyError("invoice not found")
        issuer, amount, currency, revision = row
        payload = canonical_invoice(invoice_id, issuer, amount, currency, revision)
        signature = sign_invoice(payload, private)
        algorithm = "RSA-PSS"
        record_id = signature_id(invoice_id, issuer, revision, algorithm)
        with sqlite3.connect(self.path) as db:
            db.execute("INSERT INTO signatures VALUES(?,?,?,?,?,?,?,?,?)", (record_id, invoice_id, issuer, revision, algorithm, invoice_digest(payload), payload, signature, int(time.time())))
        return record_id

    def verify_record(self, record_id: str, public) -> bool:
        with sqlite3.connect(self.path) as db:
            row = db.execute("SELECT algorithm, payload_digest, payload, signature FROM signatures WHERE signature_id=?", (record_id,)).fetchone()
        return bool(row) and row[0] == "RSA-PSS" and invoice_digest(row[2]) == row[1] and verify_invoice(row[2], row[3], public)

    def history(self, invoice_id: str):
        with sqlite3.connect(self.path) as db:
            return db.execute("SELECT signature_id, revision, created FROM signatures WHERE invoice_id=? ORDER BY revision", (invoice_id,)).fetchall()
