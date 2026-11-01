"""ApprovalFlow pqc application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from approvalflow_pqc import crypto
from approvalflow_pqc.workflow import (create_approval_request_identity, export_approval_request_public_key,
    load_approval_request_public_key, validate_approval_request, canonicalize_approval_request, sign_approval_request,
    verify_approval_request, seal_approval_request_payload, open_approval_request_payload,
    rotate_approval_request_identity, revoke_approval_request_identity, ApprovalFlowLedger,
    run_approvalflow_workflow, example_record)


def test_task_0291_identity_creation_separates_key_purposes():
    identity = create_approval_request_identity()
    assert isinstance(identity["signing_private"], crypto.mldsa.MLDSA65PrivateKey)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_0292_public_key_serialization_round_trips_by_purpose():
    identity = create_approval_request_identity()
    sign_der = export_approval_request_public_key(identity["signing_public"], "signing")
    kem_der = export_approval_request_public_key(identity["transport_public"], "transport")
    assert load_approval_request_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_approval_request_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_approval_request_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_approval_request_public_key(b"truncated", "signing")

def test_task_0293_key_purpose_and_encoding_inputs_are_strict():
    identity = create_approval_request_identity()
    with pytest.raises(ValueError): export_approval_request_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_approval_request_public_key(b"", "signing")
    with pytest.raises(ValueError): load_approval_request_public_key(b"not DER", "unknown")

def test_task_0294_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_approval_request(record) == record
    with pytest.raises(ValueError): validate_approval_request({k:v for k,v in record.items() if k != 'request_id'})
    with pytest.raises(ValueError): validate_approval_request(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid['request_id'] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_approval_request(invalid)

def test_task_0295_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_approval_request(record) == canonicalize_approval_request(reversed_record)
    assert json.loads(canonicalize_approval_request(record)) == record

def test_task_0296_signature_binds_record_and_application_context():
    identity = create_approval_request_identity()
    record = example_record()
    signed = sign_approval_request(identity, record)
    assert verify_approval_request(identity["signing_public"], record, signed)
    changed = dict(record)
    changed['payload_digest'] = "changed"
    assert not verify_approval_request(identity["signing_public"], changed, signed)
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_0297_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_approval_request_identity()
    other = create_approval_request_identity()
    record = example_record()
    signed = sign_approval_request(identity, record)
    assert not verify_approval_request(other["signing_public"], record, signed)
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_approval_request(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_approval_request(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_approval_request(identity["signing_public"], record, json.dumps(obj).encode())
    assert not verify_approval_request(identity["signing_public"], record, b"not-json")

def test_task_0298_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_approval_request_identity()
    other = create_approval_request_identity()
    record_id = str(example_record()['request_id'])
    envelope = seal_approval_request_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_approval_request_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_approval_request_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_approval_request_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_approval_request_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_approval_request_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_approval_request_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0299_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_approval_request_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_0300_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_approval_request_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_approval_request_identity()
    database = tmp_path / "records.sqlite"
    ledger = ApprovalFlowLedger(database)
    record = example_record()
    result = run_approvalflow_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(f"{record['request_id']}:{record['stage']}:{record['approver_id']}")
    assert stored == record and verify_approval_request(identity["signing_public"], stored, signature)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = ApprovalFlowLedger(database)
    stored_again, signature_again = reopened.fetch(f"{record['request_id']}:{record['stage']}:{record['approver_id']}")
    assert stored_again == record and verify_approval_request(identity["signing_public"], stored_again, signature_again)
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / 'migrated_reference'
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", 'approvalflow_pqc'], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
    ledger = ApprovalFlowLedger(tmp_path / "approvals.sqlite")
    first = dict(record, approver_id="alice")
    ledger.publish(identity, first)
    bob_identity = create_approval_request_identity()
    ledger.publish(bob_identity, dict(record, approver_id="bob"))
    assert ledger.approval_quorum_met(record["request_id"], record["stage"], 2, {"alice":identity["signing_public"],"bob":bob_identity["signing_public"]})
    with pytest.raises(ValueError): ledger.publish(identity, first)
    assert not ledger.approval_quorum_met(record["request_id"], record["stage"], 2, {"alice":identity["signing_public"]})
    ledger.close()
