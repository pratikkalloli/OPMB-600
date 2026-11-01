"""FleetPermit pqc application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from fleetpermit_pqc import crypto
from fleetpermit_pqc.workflow import (create_vehicle_permit_identity, export_vehicle_permit_public_key,
    load_vehicle_permit_public_key, validate_vehicle_permit, canonicalize_vehicle_permit, sign_vehicle_permit,
    verify_vehicle_permit, seal_vehicle_permit_payload, open_vehicle_permit_payload,
    rotate_vehicle_permit_identity, revoke_vehicle_permit_identity, FleetPermitLedger,
    run_fleetpermit_workflow, example_record)


def test_task_0311_identity_creation_separates_key_purposes():
    identity = create_vehicle_permit_identity()
    assert isinstance(identity["signing_private"], crypto.mldsa.MLDSA65PrivateKey)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_0312_public_key_serialization_round_trips_by_purpose():
    identity = create_vehicle_permit_identity()
    sign_der = export_vehicle_permit_public_key(identity["signing_public"], "signing")
    kem_der = export_vehicle_permit_public_key(identity["transport_public"], "transport")
    assert load_vehicle_permit_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_vehicle_permit_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_vehicle_permit_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_vehicle_permit_public_key(b"truncated", "signing")

def test_task_0313_key_purpose_and_encoding_inputs_are_strict():
    identity = create_vehicle_permit_identity()
    with pytest.raises(ValueError): export_vehicle_permit_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_vehicle_permit_public_key(b"", "signing")
    with pytest.raises(ValueError): load_vehicle_permit_public_key(b"not DER", "unknown")

def test_task_0314_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_vehicle_permit(record) == record
    with pytest.raises(ValueError): validate_vehicle_permit({k:v for k,v in record.items() if k != 'permit_id'})
    with pytest.raises(ValueError): validate_vehicle_permit(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid['permit_id'] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_vehicle_permit(invalid)

def test_task_0315_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_vehicle_permit(record) == canonicalize_vehicle_permit(reversed_record)
    assert json.loads(canonicalize_vehicle_permit(record)) == record

def test_task_0316_signature_binds_record_and_application_context():
    identity = create_vehicle_permit_identity()
    record = example_record()
    signed = sign_vehicle_permit(identity, record)
    assert verify_vehicle_permit(identity["signing_public"], record, signed, now=record['valid_from'] + 1)
    changed = dict(record)
    changed['valid_until'] = "changed"
    assert not verify_vehicle_permit(identity["signing_public"], changed, signed, now=record['valid_from'] + 1)
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_0317_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_vehicle_permit_identity()
    other = create_vehicle_permit_identity()
    record = example_record()
    signed = sign_vehicle_permit(identity, record)
    assert not verify_vehicle_permit(other["signing_public"], record, signed, now=record['valid_from'] + 1)
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_vehicle_permit(identity["signing_public"], record, json.dumps(obj).encode(), now=record['valid_from'] + 1)
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_vehicle_permit(identity["signing_public"], record, json.dumps(obj).encode(), now=record['valid_from'] + 1)
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_vehicle_permit(identity["signing_public"], record, json.dumps(obj).encode(), now=record['valid_from'] + 1)
    assert not verify_vehicle_permit(identity["signing_public"], record, b"not-json", now=record['valid_from'] + 1)

def test_task_0318_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_vehicle_permit_identity()
    other = create_vehicle_permit_identity()
    record_id = str(example_record()['permit_id'])
    envelope = seal_vehicle_permit_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_vehicle_permit_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_vehicle_permit_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_vehicle_permit_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_vehicle_permit_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_vehicle_permit_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_vehicle_permit_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0319_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_vehicle_permit_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_0320_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_vehicle_permit_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_vehicle_permit_identity()
    database = tmp_path / "records.sqlite"
    ledger = FleetPermitLedger(database)
    record = example_record()
    result = run_fleetpermit_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(str(record['permit_id']))
    assert stored == record and verify_vehicle_permit(identity["signing_public"], stored, signature, now=record['valid_from'] + 1)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = FleetPermitLedger(database)
    stored_again, signature_again = reopened.fetch(str(record['permit_id']))
    assert stored_again == record and verify_vehicle_permit(identity["signing_public"], stored_again, signature_again, now=record['valid_from'] + 1)
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / 'migrated_reference'
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", 'fleetpermit_pqc'], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
    signed_permit = sign_vehicle_permit(identity, record)
    assert verify_vehicle_permit(identity["signing_public"], record, signed_permit, now=record["valid_from"] + 1)
    assert not verify_vehicle_permit(identity["signing_public"], record, signed_permit, now=record["valid_until"] + 1)
