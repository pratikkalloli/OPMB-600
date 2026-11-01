"""Application and cryptographic contract tests for GenomicReportSeal."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from genomic_report_seal_pqc import crypto
from genomic_report_seal_pqc.workflow import (create_genomic_report_seal_identity, export_genomic_report_seal_public_key, load_genomic_report_seal_public_key,
    validate_genomic_report_seal_record, canonicalize_genomic_report_seal_record, sign_genomic_report_seal_record,
    verify_genomic_report_seal_record, seal_genomic_report_seal_payload, open_genomic_report_seal_payload,
    rotate_genomic_report_seal_identity, revoke_genomic_report_seal_identity, GenomicReportSealLedger,
    run_genomic_report_seal_workflow, example_record)

def test_task_0981_identity_separates_signing_and_transport_keys():
    identity = create_genomic_report_seal_identity()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_0982_public_key_encoding_round_trips_and_binds_purpose():
    identity = create_genomic_report_seal_identity()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_genomic_report_seal_public_key(identity[purpose + "_public"], purpose)
        assert load_genomic_report_seal_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_genomic_report_seal_public_key(encoded_signing, "transport")

def test_task_0983_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = create_genomic_report_seal_identity()
    encoded = export_genomic_report_seal_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_genomic_report_seal_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_genomic_report_seal_public_key(data, "signing")

def test_task_0984_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_genomic_report_seal_record(record) == record
    with pytest.raises(ValueError): validate_genomic_report_seal_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_genomic_report_seal_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_genomic_report_seal_record(invalid)
    invalid = dict(record, sequence=None)
    with pytest.raises((ValueError, TypeError)): validate_genomic_report_seal_record(invalid)

def test_task_0985_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_genomic_report_seal_record(record) == canonicalize_genomic_report_seal_record(reversed_record)
    assert json.loads(canonicalize_genomic_report_seal_record(record)) == record

def test_task_0986_signature_binds_record_context_and_validity():
    identity, record = create_genomic_report_seal_identity(), example_record()
    envelope = sign_genomic_report_seal_record(identity, record)
    assert verify_genomic_report_seal_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_genomic_report_seal_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_0987_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = create_genomic_report_seal_identity(), create_genomic_report_seal_identity(), example_record()
    envelope = sign_genomic_report_seal_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_genomic_report_seal_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_genomic_report_seal_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_genomic_report_seal_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_0988_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = create_genomic_report_seal_identity(), create_genomic_report_seal_identity()
    record_id = example_record()["record_id"]
    envelope = seal_genomic_report_seal_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_genomic_report_seal_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_genomic_report_seal_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_genomic_report_seal_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_genomic_report_seal_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0989_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_genomic_report_seal_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_0990_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_genomic_report_seal_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = create_genomic_report_seal_identity(), example_record()
    db = tmp_path / "application.sqlite"; ledger = GenomicReportSealLedger(db)
    result = run_genomic_report_seal_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_genomic_report_seal_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = GenomicReportSealLedger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "migrated_reference"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "genomic_report_seal_pqc"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
