"""Add REPO-003 candidate records from the checked-in SecurePrint source surface."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
repo_id = "REPO-003"
repo_path = "benchmark/repositories/REPO-003"
tasks = [
    ("generate_printer_keypair", "RSA-3072", "RSA key transport identity generation", "ML-KEM-768", "Replace printer RSA transport keys with ML-KEM keys while preserving one-key-per-printer isolation.", "Cryptographic key management"),
    ("generate_audit_keypair", "RSA-3072", "RSA-PSS audit signer generation", "ML-DSA-65", "Replace the audit signing key with an ML-DSA-65 signing key and retain distinct signing and KEM key purposes.", "RSA digital signature migration"),
    ("serialize_public_key", "RSA SubjectPublicKeyInfo", "Printer public-key serialization", "ML-KEM-768 SubjectPublicKeyInfo", "Update printer public-key serialization and consumers for standardized ML-KEM key encodings.", "API, dependency and compatibility migration"),
    ("load_public_key", "RSA SubjectPublicKeyInfo", "Printer public-key deserialization and type check", "ML-KEM-768", "Parse only the expected ML-KEM public-key type for printer key distribution and reject unrelated keys.", "API, dependency and compatibility migration"),
    ("encrypt_job_content", "RSA-OAEP plus AES-256-GCM", "Print-job data-key wrapping", "ML-KEM-768, HKDF-SHA-256, AES-256-GCM", "Replace RSA wrapping with ML-KEM encapsulation and context-bound HKDF key derivation without changing authenticated job encryption.", "RSA encryption and key-wrapping redesign"),
    ("decrypt_job_content", "RSA-OAEP plus AES-256-GCM", "Print-job key decapsulation and authenticated decryption", "ML-KEM-768, HKDF-SHA-256, AES-256-GCM", "Decapsulate the ML-KEM secret, derive the same job-scoped key, and reject malformed encapsulations or modified ciphertext.", "Cross-component cryptographic migration"),
    ("canonical_metadata", "SHA-256 manifest binding", "Canonical signed print metadata encoding", "ML-DSA-65 signed metadata compatibility", "Preserve deterministic metadata encoding and bind nonce, ciphertext digest, and key encapsulation digest for signature verification.", "Cross-component cryptographic migration"),
    ("sign_job_metadata", "RSA-PSS-SHA-256", "Print-job manifest signing", "ML-DSA-65", "Replace RSA-PSS signatures with ML-DSA-65 while preserving canonical manifest bytes and rejection behavior.", "RSA digital signature migration"),
    ("verify_job_metadata", "RSA-PSS-SHA-256", "Print-job manifest signature verification", "ML-DSA-65", "Verify migrated ML-DSA signatures and reject altered metadata, malformed signatures, and wrong-key signatures.", "Cross-component cryptographic migration"),
    ("deserialize_job_package", "Hex JSON wrapped-key package", "Encrypted print-package decoding", "Hex JSON ML-KEM encapsulation package", "Update package deserialization to represent an ML-KEM ciphertext separately from content ciphertext and reject malformed encodings.", "API, dependency and compatibility migration"),
]

repo = {
    "repository_id": repo_id, "name": "SecurePrint", "application_domain": "secure_print_release",
    "path": repo_path, "purpose": "Simulation of protected print-job submission, printer-bound encryption, authenticated metadata, controlled release, and cancellation.",
    "status": "candidate", "main_modules": ["src/secureprint/crypto.py", "src/secureprint/service.py"],
    "classical_cryptography": ["RSA-3072 OAEP", "RSA-3072 PSS", "AES-256-GCM"], "task_count": 10,
    "test_status": "pending", "reference_test_status": "pending",
    "verification_evidence": "reports/evidence/REPO-003/test-results.json"
}
repo_manifest_path = ROOT / "benchmark/manifests/repositories.json"
repo_manifest = json.loads(repo_manifest_path.read_text(encoding="utf-8"))
if any(item["repository_id"] == repo_id for item in repo_manifest["repositories"]):
    raise SystemExit(f"{repo_id} already exists")
repo_manifest["repositories"].append(repo)
repo_manifest_path.write_text(json.dumps(repo_manifest, indent=2) + "\n", encoding="utf-8")

task_manifest_path = ROOT / "benchmark/manifests/tasks.json"
task_manifest = json.loads(task_manifest_path.read_text(encoding="utf-8"))
new = []
for offset, (function, classical, operation, target, objective, family) in enumerate(tasks, start=21):
    task_id = f"OPMB-{offset:04d}"
    task_dir = ROOT / repo_path / "tasks" / task_id
    task_dir.mkdir(parents=True, exist_ok=False)
    record = {
        "task_id": task_id, "repository_id": repo_id, "repository_name": "SecurePrint",
        "application_domain": "secure_print_release", "repository_version": "1.0.0", "language": "Python",
        "classical_algorithm": classical, "cryptographic_operation": operation,
        "cryptographic_library": "cryptography==50.0.2",
        "source_files": ["src/secureprint/crypto.py"], "function_names": [function],
        "migration_family": family, "migration_target": target, "migration_objective": objective,
        "preconditions": ["Use synthetic print-job bytes and fictional identities.", "The current cryptographic baseline is preserved in src/secureprint/crypto.py."],
        "expected_behavior": ["Preserve printer authorization and job lifecycle behavior.", "Reject malformed inputs and cryptographic tampering."],
        "migration_requirements": ["Use the pinned standardized PQC APIs; do not implement primitives.", "Keep signing and key-establishment keys separate.", "Maintain explicit serialization and compatibility behavior."],
        "original_tests": ["tests/test_secureprint.py"], "migration_tests": ["tests/test_secureprint_pqc.py"],
        "verification_procedure": ["Run the SecurePrint original and PQC test suites.", "Verify positive round trips and negative tamper, malformed-key, and signature cases where applicable."],
        "difficulty": "medium" if offset < 28 else "hard", "original_build_status": "pending",
        "original_test_status": "pending", "reference_patch_status": "pending",
        "cryptographic_verification_status": "pending", "validation_status": "candidate",
        "known_limitations": ["Not independently reviewed or production security certified.", "The local simulation uses in-memory state and process-ephemeral keys."],
        "created_by": "OPMB-600-team", "task_path": f"{repo_path}/tasks/{task_id}",
        "reference_path": f"{repo_path}/migrated_reference/secureprint_pqc"
    }
    (task_dir / "task.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    (task_dir / "requirements.md").write_text(f"# {task_id}: {operation}\n\n{objective}\n\nTarget: {target}.\n", encoding="utf-8")
    (task_dir / "expected_behavior.md").write_text("\n".join(f"- {item}" for item in record["expected_behavior"]) + "\n", encoding="utf-8")
    (task_dir / "verification.md").write_text("\n".join(f"- {item}" for item in record["verification_procedure"]) + "\n", encoding="utf-8")
    new.append(record)
task_manifest["tasks"].extend(new)
task_manifest_path.write_text(json.dumps(task_manifest, indent=2) + "\n", encoding="utf-8")
