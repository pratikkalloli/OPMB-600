"""Application and cryptographic contract tests for ImagingReadoutSign."""
import json, os, subprocess, sys
from pathlib import Path
import pytest
from imaging_readout_sign import crypto
from imaging_readout_sign.workflow import (create_imaging_readout_sign_identity, export_imaging_readout_sign_public_key, load_imaging_readout_sign_public_key,
    validate_imaging_readout_sign_record, canonicalize_imaging_readout_sign_record, sign_imaging_readout_sign_record,
    verify_imaging_readout_sign_record, seal_imaging_readout_sign_payload, open_imaging_readout_sign_payload,
    rotate_imaging_readout_sign_identity, revoke_imaging_readout_sign_identity, ImagingReadoutSignLedger,
    run_imaging_readout_sign_workflow, example_record)

def test_task_0911_identity_separates_signing_and_transport_keys():
    identity = create_imaging_readout_sign_identity()
    assert isinstance(identity["signing_private"], crypto.SIGNING_PRIVATE)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] != identity["transport_public"]

def test_task_0912_public_key_encoding_round_trips_and_binds_purpose():
    identity = create_imaging_readout_sign_identity()
    encoded_signing = None
    for purpose in ("signing", "transport"):
        encoded = export_imaging_readout_sign_public_key(identity[purpose + "_public"], purpose)
        assert load_imaging_readout_sign_public_key(encoded, purpose) == identity[purpose + "_public"]
        if purpose == "signing": encoded_signing = encoded
    with pytest.raises(ValueError): load_imaging_readout_sign_public_key(encoded_signing, "transport")

def test_task_0913_malformed_serialization_and_wrong_purpose_are_rejected():
    identity = create_imaging_readout_sign_identity()
    encoded = export_imaging_readout_sign_public_key(identity["signing_public"], "signing")
    with pytest.raises(ValueError): load_imaging_readout_sign_public_key(encoded, "transport")
    for data in (b"", b"not-json", b'{"v":99}'):
        with pytest.raises(ValueError): load_imaging_readout_sign_public_key(data, "signing")

def test_task_0914_domain_schema_and_policy_reject_invalid_records():
    record = example_record()
    assert validate_imaging_readout_sign_record(record) == record
    with pytest.raises(ValueError): validate_imaging_readout_sign_record({key:value for key,value in record.items() if key != "record_id"})
    with pytest.raises(ValueError): validate_imaging_readout_sign_record(dict(record, unapproved="field"))
    invalid = dict(record, expires_at=record["issued_at"])
    with pytest.raises(ValueError): validate_imaging_readout_sign_record(invalid)
    invalid = dict(record, sequence=None)
    with pytest.raises((ValueError, TypeError)): validate_imaging_readout_sign_record(invalid)

def test_task_0915_canonical_record_encoding_is_stable():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_imaging_readout_sign_record(record) == canonicalize_imaging_readout_sign_record(reversed_record)
    assert json.loads(canonicalize_imaging_readout_sign_record(record)) == record

def test_task_0916_signature_binds_record_context_and_validity():
    identity, record = create_imaging_readout_sign_identity(), example_record()
    envelope = sign_imaging_readout_sign_record(identity, record)
    assert verify_imaging_readout_sign_record(identity["signing_public"], record, envelope, now=record["issued_at"] + 1)
    assert not verify_imaging_readout_sign_record(identity["signing_public"], record, envelope, now=record["expires_at"] + 1)
    assert crypto.verify_document(envelope, identity["signing_public"], b"wrong-context") is None

def test_task_0917_signature_rejects_tamper_wrong_key_and_downgrade():
    identity, other, record = create_imaging_readout_sign_identity(), create_imaging_readout_sign_identity(), example_record()
    envelope = sign_imaging_readout_sign_record(identity, record)
    now = record["issued_at"] + 1
    assert not verify_imaging_readout_sign_record(other["signing_public"], record, envelope, now=now)
    obj = json.loads(envelope); obj["alg"] = "UNSUPPORTED"
    assert not verify_imaging_readout_sign_record(identity["signing_public"], record, json.dumps(obj).encode(), now=now)
    assert not verify_imaging_readout_sign_record(identity["signing_public"], record, b"malformed", now=now)

def test_task_0918_hybrid_envelope_binds_recipient_and_record_context():
    identity, other = create_imaging_readout_sign_identity(), create_imaging_readout_sign_identity()
    record_id = example_record()["record_id"]
    envelope = seal_imaging_readout_sign_payload(identity["transport_public"], b"synthetic protected payload", record_id)
    assert open_imaging_readout_sign_payload(identity["transport_private"], envelope, record_id) == b"synthetic protected payload"
    with pytest.raises(ValueError): open_imaging_readout_sign_payload(other["transport_private"], envelope, record_id)
    with pytest.raises(ValueError): open_imaging_readout_sign_payload(identity["transport_private"], envelope, record_id + "-other")
    obj = json.loads(envelope); obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_imaging_readout_sign_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0919_rotation_retires_old_key_version():
    registry = crypto.KeyRegistry(); first = registry.provision("identity")
    second = rotate_imaging_readout_sign_identity(registry, "identity")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity", 1)
    assert registry.get_active("identity", 2)["status"] == "active"

def test_task_0920_revocation_ledger_persistence_and_cli_workflow(tmp_path):
    registry = crypto.KeyRegistry(); registry.provision("retiring"); revoke_imaging_readout_sign_identity(registry, "retiring")
    with pytest.raises(ValueError): registry.get_active("retiring", 1)
    identity, record = create_imaging_readout_sign_identity(), example_record()
    db = tmp_path / "application.sqlite"; ledger = ImagingReadoutSignLedger(db)
    result = run_imaging_readout_sign_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(record["record_id"])
    assert stored == record and verify_imaging_readout_sign_record(identity["signing_public"], stored, signature, now=record["issued_at"] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close(); reopened = ImagingReadoutSignLedger(db)
    assert reopened.fetch(record["record_id"])[0] == record; reopened.close()
    env = os.environ.copy(); package_root = Path(__file__).resolve().parents[1] / "src"
    env["PYTHONPATH"] = str(package_root) + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", "imaging_readout_sign"], cwd=Path(__file__).resolve().parents[1], input=json.dumps(record), text=True, capture_output=True, env=env)
    assert completed.returncode == 0, completed.stderr
    assert json.loads(completed.stdout)["record"] == record
