"""GeoDispatch pqc application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from geodispatch_pqc import crypto
from geodispatch_pqc.workflow import (create_dispatch_instruction_identity, export_dispatch_instruction_public_key,
    load_dispatch_instruction_public_key, validate_dispatch_instruction, canonicalize_dispatch_instruction, sign_dispatch_instruction,
    verify_dispatch_instruction, seal_dispatch_instruction_payload, open_dispatch_instruction_payload,
    rotate_dispatch_instruction_identity, revoke_dispatch_instruction_identity, GeoDispatchLedger,
    run_geodispatch_workflow, example_record)


def test_task_0261_identity_creation_separates_key_purposes():
    identity = create_dispatch_instruction_identity()
    assert isinstance(identity["signing_private"], crypto.mldsa.MLDSA65PrivateKey)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_0262_public_key_serialization_round_trips_by_purpose():
    identity = create_dispatch_instruction_identity()
    sign_der = export_dispatch_instruction_public_key(identity["signing_public"], "signing")
    kem_der = export_dispatch_instruction_public_key(identity["transport_public"], "transport")
    assert load_dispatch_instruction_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_dispatch_instruction_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_dispatch_instruction_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_dispatch_instruction_public_key(b"truncated", "signing")

def test_task_0263_key_purpose_and_encoding_inputs_are_strict():
    identity = create_dispatch_instruction_identity()
    with pytest.raises(ValueError): export_dispatch_instruction_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_dispatch_instruction_public_key(b"", "signing")
    with pytest.raises(ValueError): load_dispatch_instruction_public_key(b"not DER", "unknown")

def test_task_0264_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_dispatch_instruction(record) == record
    with pytest.raises(ValueError): validate_dispatch_instruction({k:v for k,v in record.items() if k != 'dispatch_id'})
    with pytest.raises(ValueError): validate_dispatch_instruction(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid['dispatch_id'] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_dispatch_instruction(invalid)

def test_task_0265_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_dispatch_instruction(record) == canonicalize_dispatch_instruction(reversed_record)
    assert json.loads(canonicalize_dispatch_instruction(record)) == record

def test_task_0266_signature_binds_record_and_application_context():
    identity = create_dispatch_instruction_identity()
    record = example_record()
    signed = sign_dispatch_instruction(identity, record)
    assert verify_dispatch_instruction(identity["signing_public"], record, signed)
    changed = dict(record)
    changed['expires_at'] = "changed"
    assert not verify_dispatch_instruction(identity["signing_public"], changed, signed)
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_0267_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_dispatch_instruction_identity()
    other = create_dispatch_instruction_identity()
    record = example_record()
    signed = sign_dispatch_instruction(identity, record)
    assert not verify_dispatch_instruction(other["signing_public"], record, signed)
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_dispatch_instruction(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_dispatch_instruction(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_dispatch_instruction(identity["signing_public"], record, json.dumps(obj).encode())
    assert not verify_dispatch_instruction(identity["signing_public"], record, b"not-json")

def test_task_0268_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_dispatch_instruction_identity()
    other = create_dispatch_instruction_identity()
    record_id = str(example_record()['dispatch_id'])
    envelope = seal_dispatch_instruction_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_dispatch_instruction_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_dispatch_instruction_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_dispatch_instruction_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_dispatch_instruction_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_dispatch_instruction_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_dispatch_instruction_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0269_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_dispatch_instruction_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_0270_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_dispatch_instruction_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_dispatch_instruction_identity()
    database = tmp_path / "records.sqlite"
    ledger = GeoDispatchLedger(database)
    record = example_record()
    result = run_geodispatch_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(str(record['dispatch_id']))
    assert stored == record and verify_dispatch_instruction(identity["signing_public"], stored, signature)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = GeoDispatchLedger(database)
    stored_again, signature_again = reopened.fetch(str(record['dispatch_id']))
    assert stored_again == record and verify_dispatch_instruction(identity["signing_public"], stored_again, signature_again)
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / 'migrated_reference'
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", 'geodispatch_pqc'], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
    with pytest.raises(ValueError): validate_dispatch_instruction(dict(record, destination={"lat":91,"lon":0}))
