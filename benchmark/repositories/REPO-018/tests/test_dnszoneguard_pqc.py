"""DNSZoneGuard pqc application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from dnszoneguard_pqc import crypto
from dnszoneguard_pqc.workflow import (create_zone_update_identity, export_zone_update_public_key,
    load_zone_update_public_key, validate_zone_update, canonicalize_zone_update, sign_zone_update,
    verify_zone_update, seal_zone_update_payload, open_zone_update_payload,
    rotate_zone_update_identity, revoke_zone_update_identity, DNSZoneGuardLedger,
    run_dnszoneguard_workflow, example_record)


def test_task_0171_identity_creation_separates_key_purposes():
    identity = create_zone_update_identity()
    assert isinstance(identity["signing_private"], crypto.mldsa.MLDSA65PrivateKey)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_0172_public_key_serialization_round_trips_by_purpose():
    identity = create_zone_update_identity()
    sign_der = export_zone_update_public_key(identity["signing_public"], "signing")
    kem_der = export_zone_update_public_key(identity["transport_public"], "transport")
    assert load_zone_update_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_zone_update_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_zone_update_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_zone_update_public_key(b"truncated", "signing")

def test_task_0173_key_purpose_and_encoding_inputs_are_strict():
    identity = create_zone_update_identity()
    with pytest.raises(ValueError): export_zone_update_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_zone_update_public_key(b"", "signing")
    with pytest.raises(ValueError): load_zone_update_public_key(b"not DER", "unknown")

def test_task_0174_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_zone_update(record) == record
    with pytest.raises(ValueError): validate_zone_update({k:v for k,v in record.items() if k != 'zone'})
    with pytest.raises(ValueError): validate_zone_update(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid['zone'] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_zone_update(invalid)

def test_task_0175_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_zone_update(record) == canonicalize_zone_update(reversed_record)
    assert json.loads(canonicalize_zone_update(record)) == record

def test_task_0176_signature_binds_record_and_application_context():
    identity = create_zone_update_identity()
    record = example_record()
    signed = sign_zone_update(identity, record)
    assert verify_zone_update(identity["signing_public"], record, signed)
    changed = dict(record)
    changed['published_at'] = "changed"
    assert not verify_zone_update(identity["signing_public"], changed, signed)
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_0177_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_zone_update_identity()
    other = create_zone_update_identity()
    record = example_record()
    signed = sign_zone_update(identity, record)
    assert not verify_zone_update(other["signing_public"], record, signed)
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_zone_update(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_zone_update(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_zone_update(identity["signing_public"], record, json.dumps(obj).encode())
    assert not verify_zone_update(identity["signing_public"], record, b"not-json")

def test_task_0178_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_zone_update_identity()
    other = create_zone_update_identity()
    record_id = str(example_record()['serial'])
    envelope = seal_zone_update_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_zone_update_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_zone_update_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_zone_update_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_zone_update_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_zone_update_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_zone_update_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0179_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_zone_update_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_0180_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_zone_update_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_zone_update_identity()
    database = tmp_path / "records.sqlite"
    ledger = DNSZoneGuardLedger(database)
    record = example_record()
    result = run_dnszoneguard_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(f"{record['zone']}:{record['serial']}")
    assert stored == record and verify_zone_update(identity["signing_public"], stored, signature)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = DNSZoneGuardLedger(database)
    stored_again, signature_again = reopened.fetch(f"{record['zone']}:{record['serial']}")
    assert stored_again == record and verify_zone_update(identity["signing_public"], stored_again, signature_again)
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / 'migrated_reference'
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", 'dnszoneguard_pqc'], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
    later = dict(record, serial=record["serial"] + 1)
    ledger = DNSZoneGuardLedger(tmp_path / "dns-ledger.sqlite")
    ledger.publish(identity, record)
    assert ledger.fetch(f"{record['zone']}:{record['serial']}")[0] == record
    with pytest.raises(ValueError): ledger.publish(identity, dict(record, serial=record["serial"] - 1))
    ledger.close()
