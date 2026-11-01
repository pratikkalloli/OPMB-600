import pytest

from invoiceseal.crypto import canonical_invoice, export_public_key, generate_signer, invoice_digest, load_public_key, signature_id, sign_invoice, verify_invoice
from invoiceseal.service import InvoiceSeal


def test_invoice_issue_sign_revision_history(tmp_path):
    private, public = generate_signer()
    app = InvoiceSeal(tmp_path / "invoices.db")
    app.issue("SIM-INV-1", "Example Issuer", 12500, "usd")
    record = app.sign_current("SIM-INV-1", private)
    assert app.verify_record(record, public)
    assert app.revise_amount("SIM-INV-1", 15000) == 2
    assert len(app.history("SIM-INV-1")) == 1


def test_invalid_amount_and_currency_rejected():
    with pytest.raises(ValueError):
        canonical_invoice("i", "issuer", -1, "USD", 1)
    with pytest.raises(ValueError):
        canonical_invoice("i", "issuer", 1, "US", 1)


def test_modified_payload_and_wrong_key_rejected():
    private, public = generate_signer()
    other, _ = generate_signer()
    payload = canonical_invoice("i", "issuer", 100, "USD", 1)
    signature = sign_invoice(payload, private)
    assert verify_invoice(payload, signature, public)
    assert not verify_invoice(payload + b"x", signature, public)
    assert not verify_invoice(payload, signature, other.public_key())


def test_public_key_round_trip():
    _, public = generate_signer()
    assert load_public_key(export_public_key(public)).public_numbers() == public.public_numbers()


def test_invoice_digest_and_signature_identity():
    import sqlite3

    payload = canonical_invoice("INV-9", "Synthetic Co", 540, "CAD", 3)
    assert invoice_digest(payload) != invoice_digest(payload + b"x")
    assert signature_id("INV-9", "Synthetic Co", 3) != signature_id("INV-9", "Synthetic Co", 2)
    assert signature_id("INV-9", "Synthetic Co", 3, "RSA-PSS") != signature_id("INV-9", "Synthetic Co", 3, "ML-DSA-65")


def test_persisted_payload_digest_detects_database_tampering(tmp_path):
    import sqlite3

    private, public = generate_signer()
    database = tmp_path / "tamper.db"
    app = InvoiceSeal(database)
    app.issue("INV-10", "Issuer", 220, "USD")
    record = app.sign_current("INV-10", private)
    with sqlite3.connect(database) as db:
        db.execute("UPDATE signatures SET payload_digest=? WHERE signature_id=?", ("0" * 64, record))
    assert not app.verify_record(record, public)
