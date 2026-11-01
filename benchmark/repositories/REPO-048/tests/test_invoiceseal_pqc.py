import pytest

from invoiceseal_pqc.crypto import canonical_invoice, export_public_key, generate_signer, invoice_digest, load_public_key, signature_id, sign_invoice, verify_invoice
from invoiceseal_pqc.service import InvoiceSealPQC


def test_mldsa_invoice_revision_is_historically_verifiable(tmp_path):
    private = generate_signer()
    app = InvoiceSealPQC(tmp_path / "invoices.db")
    app.issue("SIM-44", "Example Ltd", 4080, "USD")
    record = app.sign_current("SIM-44", private)
    assert app.verify_record(record, private.public_key())
    assert app.revise_amount("SIM-44", 5000) == 2
    assert app.verify_record(record, private.public_key())


def test_mldsa_rejects_modified_payload_and_wrong_key():
    private = generate_signer()
    other = generate_signer()
    payload = canonical_invoice("i", "issuer", 10, "USD", 1)
    signature = sign_invoice(payload, private)
    assert verify_invoice(payload, signature, private.public_key())
    assert not verify_invoice(payload + b"!", signature, private.public_key())
    assert not verify_invoice(payload, signature, other.public_key())


def test_mldsa_key_encoding_and_malformed_input():
    private = generate_signer()
    public = load_public_key(export_public_key(private.public_key()))
    assert verify_invoice(b"invoice", sign_invoice(b"invoice", private), public)
    with pytest.raises(ValueError):
        load_public_key(b"invalid")


def test_canonical_digest_and_record_identity():
    payload = canonical_invoice("INV-9", "Synthetic Co", 540, "CAD", 3)
    assert invoice_digest(payload) != invoice_digest(payload + b"x")
    assert signature_id("INV-9", "Synthetic Co", 3) != signature_id("INV-9", "Synthetic Co", 2)
    assert signature_id("INV-9", "Synthetic Co", 3, "ML-DSA-65") != signature_id("INV-9", "Synthetic Co", 3, "RSA-PSS")


def test_persisted_payload_digest_detects_database_tampering(tmp_path):
    import sqlite3

    private = generate_signer()
    database = tmp_path / "tamper.db"
    app = InvoiceSealPQC(database)
    app.issue("INV-10", "Issuer", 220, "USD")
    record = app.sign_current("INV-10", private)
    with sqlite3.connect(database) as db:
        db.execute("UPDATE signatures SET payload_digest=? WHERE signature_id=?", ("0" * 64, record))
    assert not app.verify_record(record, private.public_key())
