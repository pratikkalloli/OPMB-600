"""DataProvenance original application and cryptography contract tests."""
import json
import os
import subprocess
import sys
from pathlib import Path
import pytest
from dataprovenance import crypto
from dataprovenance.workflow import (create_provenance_checkpoint_identity, export_provenance_checkpoint_public_key,
    load_provenance_checkpoint_public_key, validate_provenance_checkpoint, canonicalize_provenance_checkpoint, sign_provenance_checkpoint,
    verify_provenance_checkpoint, seal_provenance_checkpoint_payload, open_provenance_checkpoint_payload,
    rotate_provenance_checkpoint_identity, revoke_provenance_checkpoint_identity, DataProvenanceLedger,
    run_dataprovenance_workflow, example_record)


def test_task_0231_identity_creation_separates_key_purposes():
    identity = create_provenance_checkpoint_identity()
    assert isinstance(identity["signing_private"], crypto.rsa.RSAPrivateKey)
    assert isinstance(identity["transport_private"], crypto.TRANSPORT_PRIVATE)
    assert identity["signing_public"] is not identity["transport_public"]

def test_task_0232_public_key_serialization_round_trips_by_purpose():
    identity = create_provenance_checkpoint_identity()
    sign_der = export_provenance_checkpoint_public_key(identity["signing_public"], "signing")
    kem_der = export_provenance_checkpoint_public_key(identity["transport_public"], "transport")
    assert load_provenance_checkpoint_public_key(sign_der, "signing") == identity["signing_public"]
    assert load_provenance_checkpoint_public_key(kem_der, "transport") == identity["transport_public"]
    with pytest.raises(ValueError): load_provenance_checkpoint_public_key(sign_der, "transport")
    with pytest.raises(ValueError): load_provenance_checkpoint_public_key(b"truncated", "signing")

def test_task_0233_key_purpose_and_encoding_inputs_are_strict():
    identity = create_provenance_checkpoint_identity()
    with pytest.raises(ValueError): export_provenance_checkpoint_public_key(identity["signing_public"], "encryption")
    with pytest.raises(ValueError): load_provenance_checkpoint_public_key(b"", "signing")
    with pytest.raises(ValueError): load_provenance_checkpoint_public_key(b"not DER", "unknown")

def test_task_0234_domain_validation_enforces_required_fields_and_policy():
    record = example_record()
    assert validate_provenance_checkpoint(record) == record
    with pytest.raises(ValueError): validate_provenance_checkpoint({k:v for k,v in record.items() if k != 'object_id'})
    with pytest.raises(ValueError): validate_provenance_checkpoint(dict(record, unexpected_field="downgrade"))
    invalid = dict(record)
    invalid['object_id'] = None
    # Domain rules reject invalid values while accepting the canonical valid example.
    with pytest.raises((ValueError, TypeError)): canonicalize_provenance_checkpoint(invalid)

def test_task_0235_canonicalization_is_deterministic():
    record = example_record()
    reversed_record = dict(reversed(list(record.items())))
    assert canonicalize_provenance_checkpoint(record) == canonicalize_provenance_checkpoint(reversed_record)
    assert json.loads(canonicalize_provenance_checkpoint(record)) == record

def test_task_0236_signature_binds_record_and_application_context():
    identity = create_provenance_checkpoint_identity()
    record = example_record()
    signed = sign_provenance_checkpoint(identity, record)
    assert verify_provenance_checkpoint(identity["signing_public"], record, signed)
    changed = dict(record)
    changed['previous_digest'] = "changed"
    assert not verify_provenance_checkpoint(identity["signing_public"], changed, signed)
    assert crypto.verify_document(signed, identity["signing_public"], b"wrong-context") is None

def test_task_0237_signature_rejects_wrong_key_and_tampered_envelope():
    identity = create_provenance_checkpoint_identity()
    other = create_provenance_checkpoint_identity()
    record = example_record()
    signed = sign_provenance_checkpoint(identity, record)
    assert not verify_provenance_checkpoint(other["signing_public"], record, signed)
    obj = json.loads(signed)
    obj["payload"] = "eA=="
    assert not verify_provenance_checkpoint(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["alg"] = "RSA-PSS-SHA256" if crypto.SIGNATURE_ALGORITHM != "RSA-PSS-SHA256" else "UNSUPPORTED"
    assert not verify_provenance_checkpoint(identity["signing_public"], record, json.dumps(obj).encode())
    obj = json.loads(signed)
    obj["v"] = 99
    assert not verify_provenance_checkpoint(identity["signing_public"], record, json.dumps(obj).encode())
    assert not verify_provenance_checkpoint(identity["signing_public"], record, b"not-json")

def test_task_0238_hybrid_envelope_authenticates_context_and_recipient():
    identity = create_provenance_checkpoint_identity()
    other = create_provenance_checkpoint_identity()
    record_id = str(example_record()['object_id'])
    envelope = seal_provenance_checkpoint_payload(identity["transport_public"], b"protected application payload", record_id)
    assert open_provenance_checkpoint_payload(identity["transport_private"], envelope, record_id) == b"protected application payload"
    with pytest.raises(ValueError): open_provenance_checkpoint_payload(identity["transport_private"], envelope, record_id + "-wrong")
    with pytest.raises(ValueError): open_provenance_checkpoint_payload(other["transport_private"], envelope, record_id)
    obj = json.loads(envelope)
    obj["ciphertext"] = obj["ciphertext"][:-4] + "AAAA"
    with pytest.raises(ValueError): open_provenance_checkpoint_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["alg"] = "UNSUPPORTED"
    with pytest.raises(ValueError): open_provenance_checkpoint_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)
    obj = json.loads(envelope)
    obj["v"] = 99
    with pytest.raises(ValueError): open_provenance_checkpoint_payload(identity["transport_private"], json.dumps(obj).encode(), record_id)

def test_task_0239_rotation_retires_old_version_and_generates_new_keys():
    registry = crypto.KeyRegistry()
    first = registry.provision("identity-a")
    second = rotate_provenance_checkpoint_identity(registry, "identity-a")
    assert first["version"] == 1 and second["version"] == 2
    with pytest.raises(ValueError): registry.get_active("identity-a", 1)
    active = registry.get_active("identity-a", 2)
    assert active["signing_private"].public_key() != crypto.load_public_key(first["signing_public"], "signing")

def test_task_0240_revocation_and_append_only_application_workflow(tmp_path):
    registry = crypto.KeyRegistry()
    registry.provision("identity-b")
    revoke_provenance_checkpoint_identity(registry, "identity-b")
    with pytest.raises(ValueError): registry.get_active("identity-b", 1)
    identity = create_provenance_checkpoint_identity()
    database = tmp_path / "records.sqlite"
    ledger = DataProvenanceLedger(database)
    record = example_record()
    result = run_dataprovenance_workflow(identity, record, ledger)
    stored, signature = ledger.fetch(f"{record['object_id']}:{record['sequence']}")
    assert stored == record and verify_provenance_checkpoint(identity["signing_public"], stored, signature)
    with pytest.raises(ValueError): ledger.publish(identity, record)
    ledger.close()
    reopened = DataProvenanceLedger(database)
    stored_again, signature_again = reopened.fetch(f"{record['object_id']}:{record['sequence']}")
    assert stored_again == record and verify_provenance_checkpoint(identity["signing_public"], stored_again, signature_again)
    reopened.close()
    environment = os.environ.copy()
    source_root = Path(__file__).resolve().parents[1] / 'src'
    environment["PYTHONPATH"] = str(source_root) + os.pathsep + environment.get("PYTHONPATH", "")
    completed = subprocess.run([sys.executable, "-m", 'dataprovenance'], cwd=Path(__file__).resolve().parents[1],
                               input=json.dumps(record), text=True, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, env=environment, check=False)
    assert completed.returncode == 0, completed.stderr
    cli_result = json.loads(completed.stdout)
    assert cli_result["record"] == record and cli_result["context"]
    second = dict(record, sequence=2, payload_digest="c"*64, previous_digest=record["payload_digest"])
    ledger = DataProvenanceLedger(tmp_path / "provenance.sqlite")
    ledger.publish(identity, record)
    ledger.publish(identity, second)
    with pytest.raises(ValueError): ledger.publish(identity, dict(second, sequence=3, previous_digest="0"*64))
    ledger.close()
