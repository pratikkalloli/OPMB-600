"""Application and cryptographic contract tests for AccreditationEvidence."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from accreditation_evidence import crypto
from accreditation_evidence.workflow import (create_accreditation_evidence_identity, export_accreditation_evidence_public_key, load_accreditation_evidence_public_key,
    validate_accreditation_evidence_record, canonicalize_accreditation_evidence_record, sign_accreditation_evidence_record,
    verify_accreditation_evidence_record, seal_accreditation_evidence_payload, open_accreditation_evidence_payload,
    rotate_accreditation_evidence_identity, revoke_accreditation_evidence_identity, AccreditationEvidenceLedger,
    run_accreditation_evidence_workflow, example_record)

def test_task_1771_identity_separates_signing_and_transport_keys():
    identity = create_accreditation_evidence_identity()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_1772_public_key_encoding_round_trips_and_binds_purpose():
    identity = create_accreditation_evidence_identity()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_accreditation_evidence_public_key(identity[purpose + "_public"], purpose)
        assert load_accreditation_evidence_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_accreditation_evidence_public_key(encoded_signing, "transport")

def test_task_1773_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = create_accreditation_evidence_identity()
    encoded = export_accreditation_evidence_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_accreditation_evidence_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_accreditation_evidence_public_key(data, "signing")

def test_task_1774_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_accreditation_evidence_record(record) == record
    with pytest.raises(ValueError): validate_accreditation_evidence_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_accreditation_evidence_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_accreditation_evidence_record(invalid)
    invalid = dict(record, sequence=None)
    with pytest.raises((ValueError, TypeError)): validate_accreditation_evidence_record(invalid)

def test_task_1775_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_accreditation_evidence_record(record) == canonicalize_accreditation_evidence_record(reversed_record)
    assert json.loads(canonicalize_accreditation_evidence_record(record)) == record

def test_task_1776_signature_binds_record_context_and_validity():
    identity, record = create_accreditation_evidence_identity(), example_record()
    envelope = sign_accreditation_evidence_record(identity, record)
    assert verify_accreditation_evidence_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_accreditation_evidence_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_1777_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = create_accreditation_evidence_identity(), create_accreditation_evidence_identity(), example_record()
    envelope = sign_accreditation_evidence_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_accreditation_evidence_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_accreditation_evidence_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_accreditation_evidence_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_1778_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = create_accreditation_evidence_identity(), create_accreditation_evidence_identity()
    record_id = example_record()["record_id"]
    envelope = seal_accreditation_evidence_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_accreditation_evidence_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_accreditation_evidence_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_accreditation_evidence_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_accreditation_evidence_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_1779_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_accreditation_evidence_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_1780_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_accreditation_evidence_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = create_accreditation_evidence_identity(), example_record()
    db = tmp_path / "application.sqlite"; ledger = AccreditationEvidenceLedger(db)
    result = run_accreditation_evidence_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_accreditation_evidence_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = AccreditationEvidenceLedger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "accreditation_evidence"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
