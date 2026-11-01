"""Build the remaining controlled Part 3 applications and task records."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "benchmark/repositories"
CATALOGUE = ROOT / "docs/application_catalogue.md"
NAMES = [
    ("TrustBridge", "service_identity", "Service identity enrollment, certificate issuance simulation, and signed trust updates", "RSA-3072 PSS", "ML-DSA-65"),
    ("FleetUpdate", "secure_firmware_updates", "Signed firmware release manifests, staged rollout approvals, and device acknowledgements", "RSA-3072 PSS", "ML-DSA-65"),
    ("CareLink", "healthcare_messaging", "Confidential clinical message exchange with recipient key establishment and audit signatures", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("PayRoute", "payment_routing", "Synthetic payment instruction signing, recipient key delivery, and idempotent settlement records", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("CodeSignHub", "software_supply_chain", "Artifact provenance attestations, release signing, and verification policy", "RSA-3072 PSS", "ML-DSA-65"),
    ("EdgeTunnel", "secure_networking", "Gateway session establishment, peer authentication, and protected telemetry envelopes", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("ArchiveSeal", "records_archiving", "Long-retention record sealing, signed indexes, and key rotation metadata", "RSA-3072 PSS", "ML-DSA-65"),
    ("DevicePair", "iot_device_enrollment", "Manufacturing-time device enrollment, ownership transfer, and signed configuration delivery", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("BuildRelay", "ci_cd_security", "CI worker identity, encrypted secret handoff, and signed build attestations", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("CaseExchange", "legal_document_exchange", "Matter-scoped document exchange, recipient access, and signed custody events", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("SensorMesh", "industrial_telemetry", "Authenticated sensor batches, gateway verification, and fleet key lifecycle", "RSA-3072 PSS", "ML-DSA-65"),
    ("IdentityCache", "identity_federation", "Federated assertion signing, verifier key distribution, and rollover behavior", "RSA-3072 PSS", "ML-DSA-65"),
    ("BackupRelay", "backup_replication", "Encrypted backup chunk transfer, replica authentication, and restore integrity", "RSA-3072 OAEP/PSS", "ML-KEM-768 + ML-DSA-65"),
    ("PolicyGate", "access_control", "Signed policy bundles, delegated approval, and auditable authorization decisions", "RSA-3072 PSS", "ML-DSA-65"),
]
TASKS = [
    ("RSA key-pair provisioning", "Cryptographic key management", "ML-DSA-65", "Replace RSA signing identity provisioning with distinct ML-DSA signing keys and explicit encoded-key validation."),
    ("Public-key serialization", "API, dependency and compatibility migration", "ML-DSA-65", "Replace RSA public-key serialization with a versioned ML-DSA encoding and reject ambiguous or truncated encodings."),
    ("Detached record signing", "RSA digital signature migration", "ML-DSA-65", "Migrate detached record signatures while preserving canonical input bytes and the caller-visible result contract."),
    ("Signature verification policy", "RSA digital signature migration", "ML-DSA-65", "Update verification to accept only the declared PQC algorithm and fail closed for malformed keys and signatures."),
    ("Recipient key establishment", "RSA encryption and key-wrapping redesign", "ML-KEM-768 + HKDF + AES-256-GCM", "Replace RSA key transport with ML-KEM encapsulation, context-bound HKDF, and authenticated wrapping of a fresh data key."),
    ("Envelope encoding", "API, dependency and compatibility migration", "Versioned ML-KEM envelope", "Define explicit algorithm and format version fields; preserve round trips and reject unknown versions without classical fallback."),
    ("Tamper and context binding", "Cross-component cryptographic migration", "ML-KEM + HKDF + AES-256-GCM", "Bind application, tenant, and record context into KDF or AEAD associated data and detect all field tampering."),
    ("Key rotation and revocation", "Cryptographic key management", "Versioned ML-DSA/ML-KEM key registry", "Add key identifiers, active/retired/revoked states, and deterministic rejection of revoked key material."),
    ("Dependency and API migration", "API, dependency and compatibility migration", "Maintained standardized PQC provider", "Update provider usage, dependency declarations, serialization call sites, and error handling without implementing primitives."),
    ("Cross-component migration and regression", "Cross-component cryptographic migration", "ML-KEM-768 + ML-DSA-65", "Migrate the complete workflow across producer, storage, and verifier; cover success, corruption, downgrade, and lifecycle regressions."),
]

def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def main():
    repos_data = json.loads((ROOT / "benchmark/manifests/repositories.json").read_text(encoding="utf-8"))
    tasks_data = json.loads((ROOT / "benchmark/manifests/tasks.json").read_text(encoding="utf-8"))
    repo_ids = {r["repository_id"] for r in repos_data["repositories"]}
    task_ids = {t["task_id"] for t in tasks_data["tasks"]}
    new_repos=[]; new_tasks=[]; catalog_rows=[]
    for index, (name, domain, purpose, classical, target) in enumerate(NAMES, start=4):
        rid=f"REPO-{index:03d}"
        if rid in repo_ids: raise RuntimeError(f"Refusing to overwrite {rid}")
        slug=name.lower(); path=BASE/rid
        if path.exists(): raise RuntimeError(f"Refusing to overwrite {path}")
        (path/"src"/slug).mkdir(parents=True); (path/"tests").mkdir(); (path/"migrated_reference"/f"{slug}_pqc").mkdir(parents=True)
        (path/"src"/slug/"__init__.py").write_text("\"\"\"Controlled OPMB-600 benchmark application.\"\"\"\n", encoding="utf-8")
        functions=[]
        for j, (op, family, task_target, objective) in enumerate(TASKS, start=1):
            fn=f"operation_{j:02d}"
            functions.append(f'''def {fn}(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:
    """Baseline {op.lower()} operation; synthetic data only."""
    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    if {j} in (1, 2, 3, 4, 8, 9, 10):
        import base64, json
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        if private_key is not None:
            signature = private_key.sign(context + b"\\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            return json.dumps({{"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}}, sort_keys=True).encode()
        try:
            envelope = json.loads(payload)
            signed_payload = base64.b64decode(envelope["payload"], validate=True)
            signature = base64.b64decode(envelope["signature"], validate=True)
            public_key.verify(signature, context + b"\\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
            return True
        except Exception:
            return False
    if private_key is not None:
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import padding
        return private_key.public_key().encrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    return public_key.decrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
''')
            tid_num=(index-1)*10+j; tid=f"OPMB-{tid_num:04d}"
            if tid in task_ids: raise RuntimeError(f"Refusing duplicate {tid}")
            task_ids.add(tid)
            task_path=f"benchmark/repositories/{rid}/tasks/{tid}"
            task={"task_id":tid,"repository_id":rid,"repository_name":name,"application_domain":domain,"repository_version":"1.0.0","language":"Python","classical_algorithm":classical,"cryptographic_operation":op,"cryptographic_library":"cryptography==50.0.2","source_files":[f"src/{slug}/crypto.py"],"function_names":[fn],"migration_family":family,"migration_target":task_target,"migration_objective":objective,"preconditions":["Use synthetic benchmark records and fictional identities only.","The original baseline is in src/"+slug+"/crypto.py."],"expected_behavior":["Preserve the documented application workflow and caller-visible success/failure contract.","Reject malformed keys, corrupted data, and unsupported versions without fallback or secret disclosure."],"migration_requirements":["Use standardized algorithms through the pinned maintained provider; do not implement primitives.","Keep ML-KEM key establishment separate from ML-DSA signatures and bind protocol context.","Update serialization, dependent call sites, and explicit key lifecycle handling."],"original_tests":["tests/test_"+slug+".py"],"migration_tests":["tests/test_"+slug+"_pqc.py"],"verification_procedure":["Run python -m pytest from the application directory.","Verify positive workflow, wrong-key, malformed encoding, tampering, and downgrade rejection as applicable.","Record provider version and machine-readable output before changing evidence statuses."],"difficulty":"hard" if j in (7,10) else "medium","original_build_status":"pending","original_test_status":"pending","reference_patch_status":"pending","cryptographic_verification_status":"pending","validation_status":"candidate","known_limitations":["Candidate specification; reference migration and independent review remain pending.","Synthetic in-memory baseline is not production security guidance."],"created_by":"OPMB-600-team","task_path":task_path,"reference_path":f"benchmark/repositories/{rid}/migrated_reference/{slug}_pqc"}
            new_tasks.append(task)
            td=BASE/rid/"tasks"/tid; td.mkdir(parents=True)
            dump(td/"task.json",task)
            for file,key in (("requirements.md","migration_requirements"),("expected_behavior.md","expected_behavior"),("verification.md","verification_procedure")):
                (td/file).write_text("# "+file.removesuffix(".md").replace("_"," ").title()+"\n\n"+"\n".join("- "+x for x in task[key])+"\n",encoding="utf-8")
        (path/"src"/slug/"crypto.py").write_text('"""Classical cryptographic operations in the synthetic '+name+' benchmark."""\nfrom __future__ import annotations\n\n'+"\n".join(functions),encoding="utf-8")
        test_body='''from cryptography.hazmat.primitives.asymmetric import rsa
from '''+slug+'''.crypto import '''+", ".join(f"operation_{j:02d}" for j in range(1,11))+'''\n\ndef test_signature_operations_roundtrip_and_reject_tampering():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public = private.public_key()
    for operation in (operation_01, operation_02, operation_03, operation_04, operation_08, operation_09, operation_10):
        envelope = operation(private, None, b"record")
        assert operation(None, public, envelope, b"opmb-v1") is True
        assert operation(None, public, envelope, b"wrong-context") is False
\ndef test_encryption_operations_roundtrip_and_input_validation():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_05, operation_06, operation_07):
        ciphertext = operation(private, None, b"short-key", b"context")
        assert operation(None, private, ciphertext, b"context") == b"short-key"
        try:
            operation(None, private, ciphertext, b"other")
        except Exception:
            pass
        else:
            raise AssertionError("wrong context must fail")
\ndef test_all_operations_reject_empty_payload():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in ('''+", ".join(f"operation_{j:02d}" for j in range(1,11))+'''):
        try:
            operation(private, private.public_key(), b"")
        except ValueError:
            pass
        else:
            raise AssertionError("empty payload must fail")
'''
        (path/"tests"/f"test_{slug}.py").write_text(test_body,encoding="utf-8")
        (path/"tests"/f"test_{slug}_pqc.py").write_text('"""Required migrated behavior tests; implement with the selected standardized provider."""\nimport pytest\n\n@pytest.mark.skip(reason="PQC reference implementation is pending; candidate task only")\ndef test_pqc_migration_contract():\n    pytest.fail("Implement PQC round-trip, tamper, downgrade, and key lifecycle cases")\n',encoding="utf-8")
        (path/"migrated_reference"/f"{slug}_pqc"/"README.md").write_text(f"# {name} PQC reference\n\nReference migration is pending. Required target: {target}. Do not mark tasks verified until implemented and tested.\n",encoding="utf-8")
        (path/"README.md").write_text(f"# {name}\n\nControlled synthetic {domain.replace('_',' ')} application for OPMB-600. {purpose}. Classical baseline: {classical}. Migration target: {target}. Candidate specifications only; no reference migration or test outcome is claimed.\n\nRun `python -m pytest` after installing the pinned requirements.\n",encoding="utf-8")
        (path/"pyproject.toml").write_text(f'[build-system]\nrequires=["setuptools>=68"]\nbuild-backend="setuptools.build_meta"\n[project]\nname="opmb-{slug}"\nversion="1.0.0"\nrequires-python=">=3.11"\ndependencies=["cryptography==50.0.2"]\n[tool.pytest.ini_options]\npythonpath=["src"]\n',encoding="utf-8")
        (path/"requirements.txt").write_text("cryptography==50.0.2\npytest==8.3.5\n",encoding="utf-8")
        new_repos.append({"repository_id":rid,"name":name,"application_domain":domain,"path":f"benchmark/repositories/{rid}","purpose":purpose+".","status":"candidate","main_modules":[f"src/{slug}/crypto.py"],"classical_cryptography":[classical,"AES-256-GCM where payload confidentiality is required"],"task_count":10,"test_status":"pending","reference_test_status":"pending"})
        catalog_rows.append(f"| {rid} | {name} | {domain.replace('_',' ')} | {purpose} | {slug}.crypto | {classical} | 10 | pending |")
        repo_ids.add(rid)
        print(f"Completed {rid} {name}: 10 task specifications, IDs OPMB-{(index-1)*10+1:04d}–OPMB-{index*10:04d}.",flush=True)
    repos_data["repositories"].extend(new_repos); tasks_data["tasks"].extend(new_tasks)
    dump(ROOT/"benchmark/manifests/repositories.json",repos_data); dump(ROOT/"benchmark/manifests/tasks.json",tasks_data)
    existing=CATALOGUE.read_text(encoding="utf-8").rstrip()+"\n"
    existing += "\n".join(catalog_rows)+"\n"
    existing += "\nAll 17 implemented applications currently contain ten candidate task specifications each. Part 3 PQC references and validation evidence remain pending until executed and reviewed.\n"
    CATALOGUE.write_text(existing,encoding="utf-8")

if __name__=="__main__": main()
