"""Application and cryptographic contract tests for FranchiseRoyaltyReport."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from franchise_royalty_report import crypto
from franchise_royalty_report.workflow import (create_franchise_royalty_report_identity, export_franchise_royalty_report_public_key, load_franchise_royalty_report_public_key,
    validate_franchise_royalty_report_record, canonicalize_franchise_royalty_report_record, sign_franchise_royalty_report_record,
    verify_franchise_royalty_report_record, seal_franchise_royalty_report_payload, open_franchise_royalty_report_payload,
    rotate_franchise_royalty_report_identity, revoke_franchise_royalty_report_identity, FranchiseRoyaltyReportLedger,
    run_franchise_royalty_report_workflow, example_record)

def test_task_2351_identity_separates_signing_and_transport_keys():
    identity = create_franchise_royalty_report_identity()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_2352_public_key_encoding_round_trips_and_binds_purpose():
    identity = create_franchise_royalty_report_identity()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_franchise_royalty_report_public_key(identity[purpose + "_public"], purpose)
        assert load_franchise_royalty_report_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_franchise_royalty_report_public_key(encoded_signing, "transport")

def test_task_2353_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = create_franchise_royalty_report_identity()
    encoded = export_franchise_royalty_report_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_franchise_royalty_report_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_franchise_royalty_report_public_key(data, "signing")

def test_task_2354_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_franchise_royalty_report_record(record) == record
    with pytest.raises(ValueError): validate_franchise_royalty_report_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_franchise_royalty_report_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_franchise_royalty_report_record(invalid)
    invalid = dict(record, quantity=None)
    with pytest.raises((ValueError, TypeError)): validate_franchise_royalty_report_record(invalid)

def test_task_2355_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_franchise_royalty_report_record(record) == canonicalize_franchise_royalty_report_record(reversed_record)
    assert json.loads(canonicalize_franchise_royalty_report_record(record)) == record

def test_task_2356_signature_binds_record_context_and_validity():
    identity, record = create_franchise_royalty_report_identity(), example_record()
    envelope = sign_franchise_royalty_report_record(identity, record)
    assert verify_franchise_royalty_report_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_franchise_royalty_report_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_2357_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = create_franchise_royalty_report_identity(), create_franchise_royalty_report_identity(), example_record()
    envelope = sign_franchise_royalty_report_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_franchise_royalty_report_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_franchise_royalty_report_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_franchise_royalty_report_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_2358_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = create_franchise_royalty_report_identity(), create_franchise_royalty_report_identity()
    record_id = example_record()["record_id"]
    envelope = seal_franchise_royalty_report_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_franchise_royalty_report_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_franchise_royalty_report_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_franchise_royalty_report_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_franchise_royalty_report_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_2359_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_franchise_royalty_report_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_2360_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_franchise_royalty_report_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = create_franchise_royalty_report_identity(), example_record()
    db = tmp_path / "application.sqlite"; ledger = FranchiseRoyaltyReportLedger(db)
    result = run_franchise_royalty_report_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_franchise_royalty_report_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = FranchiseRoyaltyReportLedger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "franchise_royalty_report"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
