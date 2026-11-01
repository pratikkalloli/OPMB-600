"""Finalize unique task prompts and consistent baseline signature tests."""
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPOS=ROOT/"benchmark/repositories"

def main():
    manifest=ROOT/"benchmark/manifests/tasks.json"
    data=json.loads(manifest.read_text(encoding="utf-8"))
    repos={r["repository_id"]:r for r in json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8"))["repositories"]}
    for task in data["tasks"]:
        if task["repository_id"] < "REPO-004": continue
        repo=repos[task["repository_id"]]
        original=task["migration_objective"]
        prefix=f"For {repo['name']}: "
        while original.startswith(prefix): original=original[len(prefix):]
        task["migration_objective"]=f"Within {repo['name']}'s {repo['purpose'].rstrip('.')}, {original[0].lower()+original[1:]}"
        task_dir=ROOT/task["task_path"]
        (task_dir/"task.json").write_text(json.dumps(task,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    manifest.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    for rid,repo in repos.items():
        if rid < "REPO-004": continue
        slug=repo["name"].lower(); root=REPOS/rid
        source=root/"src"/slug/"crypto.py"
        text=source.read_text(encoding="utf-8")
        text=text.replace("    if 1 in (1, 2, 3, 4, 8, 9, 10):", "    if TASK_SIGNATURES:") if False else text
        # Signatures use a small JSON envelope so the verifier receives both signed bytes and signature.
        text=text.replace("    if ", "    if ", 1)
        def operation(match):
            number=int(match.group(1)); doc=match.group(2)
            if number in (1,2,3,4,8,9,10):
                body='''    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    import base64, json
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        signature = private_key.sign(context + b"\\x00" + payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return json.dumps({"payload": base64.b64encode(payload).decode(), "signature": base64.b64encode(signature).decode()}, sort_keys=True).encode()
    try:
        envelope = json.loads(payload)
        signed_payload = base64.b64decode(envelope["payload"], validate=True)
        signature = base64.b64decode(envelope["signature"], validate=True)
        public_key.verify(signature, context + b"\\x00" + signed_payload, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except Exception:
        return False
'''
            else:
                body='''    if not isinstance(payload, bytes) or not payload:
        raise ValueError("payload must be non-empty bytes")
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.asymmetric import padding
    if private_key is not None:
        return private_key.public_key().encrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
    return public_key.decrypt(payload, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=context))
'''
            return f'def operation_{number:02d}(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1") -> bytes | bool:\n    {doc}\n'+body
        text=re.sub(r'def operation_(\d\d)\(private_key, public_key, payload: bytes, context: bytes = b"opmb-v1"\) -> bytes \| bool:\n    (""".*?""")\n.*?(?=\ndef operation_|\Z)',operation,text,flags=re.S)
        text=text.replace('b\\"opmb-v1\\"','b"opmb-v1"')
        source.write_text(text,encoding="utf-8")
        (root/"tests"/f"test_{slug}.py").write_text(f'''from cryptography.hazmat.primitives.asymmetric import rsa
from {slug}.crypto import operation_01, operation_02, operation_03, operation_04, operation_05, operation_06, operation_07, operation_08, operation_09, operation_10

def test_signature_envelopes_roundtrip_and_context_binding():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_01, operation_02, operation_03, operation_04, operation_08, operation_09, operation_10):
        envelope = operation(private, None, b"record")
        assert operation(None, private.public_key(), envelope, b"opmb-v1") is True
        assert operation(None, private.public_key(), envelope, b"wrong-context") is False

def test_oaep_operations_roundtrip_and_context_binding():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_05, operation_06, operation_07):
        ciphertext = operation(private, None, b"synthetic-data-key", b"context")
        assert operation(None, private, ciphertext, b"context") == b"synthetic-data-key"
        try:
            operation(None, private, ciphertext, b"other")
        except Exception:
            pass
        else:
            raise AssertionError("context mismatch must fail")

def test_every_operation_rejects_empty_input():
    private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    for operation in (operation_01, operation_02, operation_03, operation_04, operation_05, operation_06, operation_07, operation_08, operation_09, operation_10):
        try:
            operation(private, private.public_key(), b"")
        except ValueError:
            pass
        else:
            raise AssertionError("empty payload must fail")
''',encoding="utf-8")
    print("Updated 140 application-specific objectives and 14 baseline test suites.")

if __name__=="__main__": main()
