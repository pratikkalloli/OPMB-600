"""Application and cryptographic contract tests for ArchivesTransfer."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from archives_transfer_pqc import crypto
from archives_transfer_pqc.workflow import (create_archives_transfer_identity, export_archives_transfer_public_key, load_archives_transfer_public_key,
    validate_archives_transfer_record, canonicalize_archives_transfer_record, sign_archives_transfer_record,
    verify_archives_transfer_record, seal_archives_transfer_payload, open_archives_transfer_payload,
    rotate_archives_transfer_identity, revoke_archives_transfer_identity, ArchivesTransferLedger,
    run_archives_transfer_workflow, example_record)

def test_task_2041_identity_separates_signing_and_transport_keys():
    identity = create_archives_transfer_identity()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_2042_public_key_encoding_round_trips_and_binds_purpose():
    identity = create_archives_transfer_identity()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_archives_transfer_public_key(identity[purpose + "_public"], purpose)
        assert load_archives_transfer_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_archives_transfer_public_key(encoded_signing, "transport")

def test_task_2043_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = create_archives_transfer_identity()
    encoded = export_archives_transfer_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_archives_transfer_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_archives_transfer_public_key(data, "signing")

def test_task_2044_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_archives_transfer_record(record) == record
    with pytest.raises(ValueError): validate_archives_transfer_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_archives_transfer_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_archives_transfer_record(invalid)
    invalid = dict(record, filing_sequence=None)
    with pytest.raises((ValueError, TypeError)): validate_archives_transfer_record(invalid)

def test_task_2045_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_archives_transfer_record(record) == canonicalize_archives_transfer_record(reversed_record)
    assert json.loads(canonicalize_archives_transfer_record(record)) == record

def test_task_2046_signature_binds_record_context_and_validity():
    identity, record = create_archives_transfer_identity(), example_record()
    envelope = sign_archives_transfer_record(identity, record)
    assert verify_archives_transfer_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_archives_transfer_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_2047_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = create_archives_transfer_identity(), create_archives_transfer_identity(), example_record()
    envelope = sign_archives_transfer_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_archives_transfer_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_archives_transfer_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_archives_transfer_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_2048_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = create_archives_transfer_identity(), create_archives_transfer_identity()
    record_id = example_record()["record_id"]
    envelope = seal_archives_transfer_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_archives_transfer_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_archives_transfer_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_archives_transfer_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_archives_transfer_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_2049_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_archives_transfer_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_2050_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_archives_transfer_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = create_archives_transfer_identity(), example_record()
    db = tmp_path / "application.sqlite"; ledger = ArchivesTransferLedger(db)
    result = run_archives_transfer_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_archives_transfer_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = ArchivesTransferLedger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "migrated_reference"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "archives_transfer_pqc"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
