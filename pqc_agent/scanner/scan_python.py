"""Simple transparent scanner for classical public-key calls in Python source."""
from __future__ import annotations
import re
from pathlib import Path
PATTERNS={
    "RSA":re.compile(r"\brsa\b|\bRSA\b|OAEP|PSS"),
    "ECDSA/ECDH":re.compile(r"\bECDSA\b|\bECDH\b|ec\.generate_private_key|ec\.ECDSA|exchange\("),
    "X25519/X448":re.compile(r"X25519|X448"),
}
def scan(root:Path)->dict:
    findings=[]
    for source in sorted(root.rglob("*.py")):
        for line_number,line in enumerate(source.read_text(encoding="utf-8").splitlines(),1):
            for family,pattern in PATTERNS.items():
                if pattern.search(line): findings.append({"file":source.relative_to(root).as_posix(),"line":line_number,"family":family,"source":line.strip()})
    return {"scope":str(root),"classical_public_key_families_scanned":list(PATTERNS),"findings":findings,"symmetric_aead_expected":"AES-GCM is retained as payload encryption and is outside the public-key migration scan.","scope_limit":"Lexical source scan only; it does not inspect dependencies, dynamic code, serialized data, or runtime behavior."}
def main()->int:
    import argparse,json
    parser=argparse.ArgumentParser(); parser.add_argument("path",type=Path); parser.add_argument("--output",type=Path); args=parser.parse_args(); result=scan(args.path)
    rendered=json.dumps(result,indent=2); print(rendered)
    if args.output: args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(rendered+"\n",encoding="utf-8")
    return 0
if __name__=="__main__": raise SystemExit(main())
