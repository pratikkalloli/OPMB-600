#!/usr/bin/env python3
"""Build assigned Team B applications from reviewed domain specifications.

This utility writes only the explicitly selected assigned repository IDs and
Team B contribution artifacts. It refuses to overwrite any existing path.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TEAM = Path(__file__).resolve().parent
TASK_NAMES = [
    ("validate_record", "Validate the domain record and its lifecycle state"),
    ("canonical_record", "Canonicalize the complete domain record for signing"),
    ("generate_signer", "Generate an application-specific signature key pair"),
    ("sign_record", "Sign a scoped domain record with versioned context"),
    ("verify_record", "Verify a record signature and reject changed records"),
    ("export_public_key", "Serialize the verification key in the algorithm format"),
    ("load_public_key", "Load and validate a serialized verification key"),
    ("seal_artifact", "Protect a workflow artifact for an authorized recipient"),
    ("open_artifact", "Recover an artifact and reject malformed or altered envelopes"),
    ("transition_record", "Apply only an allowed domain lifecycle transition"),
]


def write(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def jwrite(path: Path, value: object) -> None:
    write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def app_sources(s: dict) -> tuple[str, str, str, str]:
    slug, entity = s["slug"], s["entity"]
    rule, kind, scope = s["rule_field"], s["rule_kind"], s["scope_field"]
    title, states, transitions = s["name"], s["states"], s["transitions"]
    fields = s["fields"]
    valid_rule = {
        "sha256": f"isinstance(value, str) and re.fullmatch(r'[0-9a-f]{{64}}', value) is not None",
        "token": f"isinstance(value, str) and re.fullmatch(r'[A-Z0-9]+(?:-[A-Z0-9]+)*', value) is not None and 4 <= len(value) <= 32",
        "bounded_microns": "type(value) is int and 0 <= value <= 5000",
        "bounded_int": "type(value) is int and 0 <= value <= 1000",
        "nonnegative": "type(value) is int and value >= 0",
        "nonnegative_int": "type(value) is int and value >= 0",
        "severity": "value in {'low', 'medium', 'high', 'critical'}",
        "enum": "value in {'minor', 'major', 'critical'}",
        "positive_epoch": "type(value) is int and value > 0",
        "positive_int": "type(value) is int and value > 0",
    }.get(kind, "value is not None")
    domain = f'''"""{title}: synthetic {entity.replace('_', ' ')} workflow."""
from __future__ import annotations
import json, re
from typing import Any

STATES = {states!r}
TRANSITIONS = {transitions!r}
REQUIRED_FIELDS = {fields!r}
RULE_FIELD = {rule!r}
SCOPE_FIELD = {scope!r}

def validate_record(record: dict[str, Any]) -> dict[str, Any]:
    """Validate a synthetic {entity.replace('_', ' ')} record."""
    if not isinstance(record, dict) or set(REQUIRED_FIELDS) - record.keys():
        raise ValueError("record is missing required workflow fields")
    if not isinstance(record.get("record_id"), str) or not record["record_id"].strip():
        raise ValueError("record_id must be a nonempty string")
    if not isinstance(record.get(SCOPE_FIELD), str) or not record[SCOPE_FIELD].strip():
        raise ValueError("workflow scope must be a nonempty string")
    if any(isinstance(record[k], str) and not record[k].strip() for k in REQUIRED_FIELDS if k not in {RULE_FIELD, "state"}):
        raise ValueError("string workflow fields must be nonempty")
    if record["state"] not in STATES:
        raise ValueError("unknown {entity.replace('_', ' ')} state")
    value = record[RULE_FIELD]
    if not ({valid_rule}):
        raise ValueError("invalid {rule.replace('_', ' ')}")
    return dict(record)

def canonical_record(record: dict[str, Any]) -> bytes:
    """Return deterministic JSON for a validated {entity.replace('_', ' ')}."""
    return json.dumps(validate_record(record), sort_keys=True, separators=(",", ":")).encode("utf-8")

def transition_record(record: dict[str, Any], new_state: str) -> dict[str, Any]:
    """Apply the {title} lifecycle without permitting skipped transitions."""
    current = validate_record(record)
    if new_state not in TRANSITIONS[current["state"]]:
        raise ValueError(f"transition {{current['state']}} -> {{new_state}} is not permitted")
    current["state"] = new_state
    return validate_record(current)
'''
    classical = '''"""Classical RSA-PSS and RSA-OAEP/AES-GCM operations."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os, json, base64
from .domain import canonical_record

CONTEXT = b"OPMB-600/'''+slug+'''/record/v1"
def generate_signer(): return rsa.generate_private_key(public_exponent=65537, key_size=3072)
def sign_record(record, private): return private.sign(CONTEXT + b"\\0" + canonical_record(record), padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
def verify_record(record, signature, public):
    try: public.verify(signature, CONTEXT + b"\\0" + canonical_record(record), padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256()); return True
    except (InvalidSignature, ValueError, TypeError): return False
def export_public_key(public): return public.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo)
def load_public_key(data):
    key=serialization.load_pem_public_key(data)
    if not isinstance(key, rsa.RSAPublicKey): raise ValueError("expected RSA verification key")
    return key
def seal_artifact(payload: bytes, recipient):
    key=os.urandom(32); nonce=os.urandom(12); aad=b"OPMB-600/'''+slug+'''/artifact/v1"
    ciphertext=AESGCM(key).encrypt(nonce,payload,aad)
    wrapped=recipient.encrypt(key,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=aad))
    return json.dumps({"v":1,"alg":"RSA-OAEP+AES-256-GCM","nonce":base64.b64encode(nonce).decode(),"key":base64.b64encode(wrapped).decode(),"ct":base64.b64encode(ciphertext).decode()},sort_keys=True,separators=(",",":")).encode()
def open_artifact(envelope: bytes, private):
    try:
        obj=json.loads(envelope); assert obj["v"]==1 and obj["alg"]=="RSA-OAEP+AES-256-GCM"
        aad=b"OPMB-600/'''+slug+'''/artifact/v1"; nonce=base64.b64decode(obj["nonce"],validate=True); wrapped=base64.b64decode(obj["key"],validate=True); ct=base64.b64decode(obj["ct"],validate=True)
        if len(nonce)!=12: raise ValueError("bad nonce")
        key=private.decrypt(wrapped,padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),algorithm=hashes.SHA256(),label=aad))
        if len(key)!=32: raise ValueError("bad data key")
        return AESGCM(key).decrypt(nonce,ct,aad)
    except Exception as exc: raise ValueError("invalid or unauthenticated artifact envelope") from exc
'''
    pqc = '''"""Separate FIPS 203 ML-KEM and FIPS 204 ML-DSA reference operations."""
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric import mldsa, mlkem
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import os, json, base64
from .domain import canonical_record

CONTEXT=b"OPMB-600/'''+slug+'''/record/v1"
AAD=b"OPMB-600/'''+slug+'''/artifact/v1"
def generate_signer(): return mldsa.MLDSA65PrivateKey.generate()
def sign_record(record, private): return private.sign(CONTEXT+b"\\0"+canonical_record(record), context=b"opmb600-'''+slug+'''-v1")
def verify_record(record, signature, public):
    try: public.verify(signature, CONTEXT+b"\\0"+canonical_record(record), context=b"opmb600-'''+slug+'''-v1"); return True
    except (InvalidSignature, ValueError, TypeError): return False
def export_public_key(public): return b"MLDSA65v1:"+public.public_bytes_raw()
def load_public_key(data):
    if not data.startswith(b"MLDSA65v1:"): raise ValueError("unknown verification key version")
    return mldsa.MLDSA65PublicKey.from_public_bytes(data[len(b"MLDSA65v1:"):])
def generate_recipient(): return mlkem.MLKEM768PrivateKey.generate()
def seal_artifact(payload: bytes, recipient_public):
    shared, encapsulation=recipient_public.encapsulate()
    key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=AAD+encapsulation).derive(shared)
    nonce=os.urandom(12); ciphertext=AESGCM(key).encrypt(nonce,payload,AAD+encapsulation)
    return json.dumps({"v":1,"kem":"ML-KEM-768","aead":"AES-256-GCM","enc":base64.b64encode(encapsulation).decode(),"nonce":base64.b64encode(nonce).decode(),"ct":base64.b64encode(ciphertext).decode()},sort_keys=True,separators=(",",":")).encode()
def open_artifact(envelope: bytes, recipient_private):
    try:
        obj=json.loads(envelope); assert obj["v"]==1 and obj["kem"]=="ML-KEM-768" and obj["aead"]=="AES-256-GCM"
        enc=base64.b64decode(obj["enc"],validate=True); nonce=base64.b64decode(obj["nonce"],validate=True); ct=base64.b64decode(obj["ct"],validate=True)
        if len(nonce)!=12: raise ValueError("bad nonce")
        shared=recipient_private.decapsulate(enc); key=HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=AAD+enc).derive(shared)
        return AESGCM(key).decrypt(nonce,ct,AAD+enc)
    except Exception as exc: raise ValueError("invalid or unauthenticated artifact envelope") from exc
'''
    return domain, classical, pqc, title


def build(s: dict) -> list[dict]:
    rid = s["repository_id"]
    n = int(rid[-3:])
    task_ids = [f"OPMB-{n*10-9+i:04d}" for i in range(10)]
    app = ROOT / "benchmark" / "repositories" / rid
    if app.exists():
        raise FileExistsError(f"assigned application already exists: {app}")
    domain, classical, pqc, title = app_sources(s)
    pkg = s["slug"]
    files = {
        "README.md": f"# {title}\n\n{s['purpose']}\n\nWorkflow: {s['workflow']}\n\nAll identifiers and records are synthetic. The original uses RSA-3072 PSS and RSA-OAEP with AES-256-GCM. The separate reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM. This benchmark reference is not production security guidance.\n\nRun `python -m pytest tests/test_{pkg}.py` and `python -m pytest tests/test_{pkg}_pqc.py` from this directory.\n",
        "requirements.txt": "cryptography==50.0.2\npytest==8.4.2\n",
        "pyproject.toml": f"[build-system]\nrequires = [\"setuptools>=68\"]\nbuild-backend = \"setuptools.build_meta\"\n\n[project]\nname = \"opmb-{pkg.replace('_','-')}\"\nversion = \"1.0.0\"\nrequires-python = \">=3.11\"\ndependencies = [\"cryptography==50.0.2\"]\n\n[tool.pytest.ini_options]\npythonpath = [\"src\", \"migrated_reference\"]\n",
    }
    for rel, text in files.items(): write(app / rel, text)
    write(app / "src" / pkg / "__init__.py", f'"""{title} original application."""\n')
    write(app / "src" / pkg / "domain.py", domain)
    write(app / "src" / pkg / "crypto.py", classical)
    write(app / "src" / pkg / "service.py", f'''"""Persistent event log for {title}."""
import json, sqlite3
from pathlib import Path
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record

class {title}:
    def __init__(self, path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS signatures(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
    def register(self, record):
        item=validate_record(record)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?)",(item["record_id"],json.dumps(item,sort_keys=True)))
    def retrieve(self, record_id):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None: raise KeyError("{s['entity'].replace('_',' ')} not found")
        return validate_record(json.loads(row[0]))
    def approve(self, record_id, private):
        record=self.retrieve(record_id); payload=canonical_record(record); sig=sign_record(record,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT OR REPLACE INTO signatures VALUES(?,?,?)",(record_id,payload,sig))
        return sig
    def verify_approval(self, record_id, public):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body,signature FROM signatures WHERE record_id=?",(record_id,)).fetchone()
        if row is None: return False
        return verify_record(self.retrieve(record_id),row[1],public) and row[0]==canonical_record(self.retrieve(record_id))
    def advance(self, record_id, state):
        record=transition_record(self.retrieve(record_id),state)
        with sqlite3.connect(self.path) as db: db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(record,sort_keys=True),record_id))
        return record
''')
    write(app / "migrated_reference" / f"{pkg}_pqc" / "__init__.py", f'"""{title} separate PQC reference."""\n')
    write(app / "migrated_reference" / f"{pkg}_pqc" / "domain.py", domain)
    write(app / "migrated_reference" / f"{pkg}_pqc" / "crypto.py", pqc)
    write(app / "migrated_reference" / f"{pkg}_pqc" / "service.py", f'''"""PQC-backed persistent event log for {title}."""
import json, sqlite3
from .domain import validate_record, transition_record, canonical_record
from .crypto import sign_record, verify_record
class {title}PQC:
    def __init__(self,path):
        self.path=str(path)
        with sqlite3.connect(self.path) as db:
            db.execute("CREATE TABLE IF NOT EXISTS records(record_id TEXT PRIMARY KEY, body TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS signatures(record_id TEXT PRIMARY KEY, body BLOB NOT NULL, signature BLOB NOT NULL)")
    def register(self,record):
        item=validate_record(record)
        with sqlite3.connect(self.path) as db: db.execute("INSERT INTO records VALUES(?,?)",(item["record_id"],json.dumps(item,sort_keys=True)))
    def retrieve(self,record_id):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body FROM records WHERE record_id=?",(record_id,)).fetchone()
        if row is None: raise KeyError("record not found")
        return validate_record(json.loads(row[0]))
    def approve(self,record_id,private):
        record=self.retrieve(record_id); payload=canonical_record(record); sig=sign_record(record,private)
        with sqlite3.connect(self.path) as db: db.execute("INSERT OR REPLACE INTO signatures VALUES(?,?,?)",(record_id,payload,sig))
        return sig
    def verify_approval(self,record_id,public):
        with sqlite3.connect(self.path) as db: row=db.execute("SELECT body,signature FROM signatures WHERE record_id=?",(record_id,)).fetchone()
        if row is None: return False
        return row[0]==canonical_record(self.retrieve(record_id)) and verify_record(self.retrieve(record_id),row[1],public)
    def advance(self,record_id,state):
        record=transition_record(self.retrieve(record_id),state)
        with sqlite3.connect(self.path) as db: db.execute("UPDATE records SET body=? WHERE record_id=?",(json.dumps(record,sort_keys=True),record_id))
        return record
''')
    write(app / "tests" / f"test_{pkg}.py", tests_text(s, False))
    write(app / "tests" / f"test_{pkg}_pqc.py", tests_text(s, True))
    tasks=[]
    for ix, (fn, objective) in enumerate(TASK_NAMES):
        tid=task_ids[ix]
        alg = "ML-KEM-768 and AES-256-GCM" if fn in {"seal_artifact","open_artifact"} else "ML-DSA-65"
        migration = "KEM confidentiality migration" if fn in {"seal_artifact","open_artifact"} else "digital signature migration"
        mobj=f"Migrate {title} {objective.lower()} from {s['classical_signature'] if migration.startswith('digital') else s['classical_key_establishment']} to {alg}, retaining {s['workflow']} semantics."
        task={"task_id":tid,"repository_id":rid,"repository_name":title,"application_domain":s["domain_group"],"repository_version":"1.0.0","language":"Python","classical_algorithm":s["classical_signature"] if migration.startswith('digital') else s["classical_key_establishment"],"cryptographic_operation":f"{fn} for {s['entity'].replace('_',' ')} workflow","cryptographic_library":"cryptography==50.0.2","source_files":[f"src/{pkg}/domain.py",f"src/{pkg}/crypto.py",f"src/{pkg}/service.py"],"function_names":[fn],"migration_family":migration,"migration_target":alg,"migration_objective":mobj,"preconditions":[f"{title} original tests pass.","All workflow data is synthetic."],"expected_behavior":[f"Preserve {s['scope_field']} and {s['rule_field']} semantics.","Reject malformed inputs, altered payloads and wrong keys.","Reject unsupported algorithm and envelope versions."],"migration_requirements":[f"Bind {s['entity']} version and application context into cryptographic operations.","Use separate signing and encapsulation keys.","Do not silently fall back to classical cryptography."],"original_tests":[f"tests/test_{pkg}.py"],"migration_tests":[f"tests/test_{pkg}_pqc.py"],"verification_procedure":["Run the original and PQC test files separately.","Check valid workflow, malformed record, tamper, wrong-key, key encoding and lifecycle transition behavior."],"difficulty":"medium","original_build_status":"pending","original_test_status":"pending","reference_patch_status":"candidate","cryptographic_verification_status":"pending","validation_status":"candidate","known_limitations":["Synthetic benchmark application; not production security guidance.","Candidate pending independent review."],"created_by":"OPMB-600-team","task_path":f"benchmark/repositories/{rid}/tasks/{tid}","reference_path":f"benchmark/repositories/{rid}/migrated_reference/{pkg}_pqc","original_test_evidence":f"reports/evidence/{rid}/test-results.json","reference_test_evidence":f"reports/evidence/{rid}/test-results.json","cryptographic_verification_evidence":f"reports/evidence/{rid}/crypto-verification.json","post_migration_scanner_evidence":f"reports/evidence/{rid}/post-migration-scan.json"}
        tasks.append(task)
        td=app/"tasks"/tid
        jwrite(td/"task.json",task)
        write(td/"requirements.md",f"# {tid}: {objective}\n\nThe migration must preserve the {s['workflow']} business invariant and the {s['scope_field']} scope.\n\n- Keep cryptographic key roles separate.\n- Bind an explicit version and {title} context.\n- Reject malformed encodings and tampered input.\n- Never use a classical fallback.\n")
        write(td/"expected_behavior.md",f"# Expected behavior\n\n{mobj}\n\nValid {s['entity'].replace('_',' ')} operations remain interoperable with the documented PQC format. Invalid state, bad {s['rule_field']}, altered content, wrong keys, and unsupported versions are rejected.\n")
        write(td/"verification.md",f"# Verification\n\nFrom `benchmark/repositories/{rid}`, run `python -m pytest tests/test_{pkg}.py` and `python -m pytest tests/test_{pkg}_pqc.py`. Exercise `{fn}`, successful behavior, tampering, wrong-key or malformed input rejection, and the named lifecycle constraints. Record exact output under `reports/evidence/{rid}/`.\n")
    repo_entry={"repository_id":rid,"name":title,"application_domain":s["domain_group"],"path":f"benchmark/repositories/{rid}","purpose":s["purpose"],"status":"candidate","tasks":task_ids,"batch":s["batch"]}
    return [repo_entry,*tasks]


def tests_text(s: dict, is_pqc: bool) -> str:
    pkg=s["slug"]; title=s["name"]; name=f"{title}PQC" if is_pqc else title
    mod=f"migrated_reference.{pkg}_pqc" if is_pqc else f"src.{pkg}"
    # run with project pythonpath; import via pytest-added src paths
    import_line=f"from {pkg}.domain import validate_record, canonical_record, transition_record\nfrom {pkg}.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, seal_artifact, open_artifact"
    if is_pqc:
        import_line=f"from {pkg}_pqc.domain import validate_record, canonical_record, transition_record\nfrom {pkg}_pqc.crypto import generate_signer, sign_record, verify_record, export_public_key, load_public_key, generate_recipient, seal_artifact, open_artifact"
    record=json.dumps(s["sample"])
    return f'''"""Application and crypto tests for {title}{' PQC reference' if is_pqc else ''}."""
import json, pytest
{import_line}

RECORD={record}
def test_domain_record_and_lifecycle():
    assert validate_record(RECORD)==RECORD
    assert canonical_record(RECORD)==canonical_record(dict(RECORD))
    changed=transition_record(RECORD,{s['transitions'][s['sample']['state']][0]!r})
    assert changed["state"]!={s['sample']['state']!r}
    with pytest.raises(ValueError): transition_record(RECORD,"impossible")
def test_domain_rule_rejects_invalid_value():
    invalid=dict(RECORD); invalid.update({json.dumps(s['invalid'])})
    with pytest.raises(ValueError): validate_record(invalid)
def test_signature_roundtrip_and_tamper_rejection():
    private=generate_signer(); public=private.public_key(); signature=sign_record(RECORD,private)
    assert verify_record(RECORD,signature,public)
    altered=dict(RECORD); altered["record_id"]+="-changed"
    assert not verify_record(altered,signature,public)
    assert not verify_record(RECORD,signature,generate_signer().public_key())
    assert load_public_key(export_public_key(public)).public_bytes_raw()==export_public_key(public).split(b":",1)[-1] if {str(is_pqc)} else load_public_key(export_public_key(public)).public_numbers()==public.public_numbers()
def test_artifact_envelope_integrity():
    if {str(is_pqc)}:
        recipient=generate_recipient(); private=recipient; public=recipient.public_key()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072); public=private.public_key()
    envelope=seal_artifact(b"{title} synthetic artifact",public)
    assert open_artifact(envelope,private)==b"{title} synthetic artifact"
    obj=json.loads(envelope); obj["ct"]=obj["ct"][:-4]+("AAAA" if obj["ct"][-4:]!="AAAA" else "BBBB")
    with pytest.raises(ValueError): open_artifact(json.dumps(obj).encode(),private)
    if {str(is_pqc)}:
        wrong=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        wrong=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(envelope,wrong)
def test_unknown_envelope_version_rejected():
    if {str(is_pqc)}:
        private=generate_recipient()
    else:
        from cryptography.hazmat.primitives.asymmetric import rsa
        private=rsa.generate_private_key(public_exponent=65537,key_size=3072)
    with pytest.raises(ValueError): open_artifact(b'{{"v":2,"alg":"unknown"}}',private)
def test_persistent_application_approval_and_stale_record_rejection(tmp_path):
    from {('migrated_reference.'+pkg+'_pqc.service' if is_pqc else pkg+'.service')} import {name}
    app={name}(tmp_path/"workflow.sqlite3")
    app.register(RECORD)
    signer=generate_signer()
    app.approve(RECORD["record_id"],signer)
    assert app.verify_approval(RECORD["record_id"],signer.public_key())
    moved=app.advance(RECORD["record_id"],{s['transitions'][s['sample']['state']][0]!r})
    assert moved["state"]!={s['sample']['state']!r}
    assert not app.verify_approval(RECORD["record_id"],signer.public_key())
'''


def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument("--batch", type=int, required=True); a=p.parse_args()
    specs=json.loads((TEAM/"application_specs.json").read_text(encoding="utf-8"))
    batch=[x for x in specs if x["batch"]==a.batch]
    if len(batch)!=10: raise SystemExit(f"batch {a.batch} requires exactly 10 reviewed specs; found {len(batch)}")
    ids=[int(x["repository_id"][-3:]) for x in batch]
    if ids!=list(range(min(ids),min(ids)+10)): raise SystemExit("batch IDs are not continuous")
    repo_manifest=[]; task_manifest=[]
    for spec in batch:
        entries=build(spec); repo_manifest.append(entries[0]); task_manifest.extend(entries[1:])
    out=TEAM/f"batch-{a.batch:02d}"
    out.mkdir(parents=True,exist_ok=False)
    jwrite(out/"repositories.json",repo_manifest); jwrite(out/"tasks.json",task_manifest)
    print(f"Generated {len(repo_manifest)} application projects and {len(task_manifest)} task records for batch {a.batch}.")

if __name__=="__main__": main()
