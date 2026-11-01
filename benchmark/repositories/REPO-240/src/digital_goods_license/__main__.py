"""Command-line entry point for DigitalGoodsLicense."""
import json, sys
from pathlib import Path
from .workflow import create_digital_goods_license_identity, run_digital_goods_license_workflow

def main(argv=None) -> int:
    try:
        raw = Path(argv[0]).read_text(encoding="utf-8") if argv else sys.stdin.read()
        result = run_digital_goods_license_workflow(create_digital_goods_license_identity(), json.loads(raw))
        print(json.dumps({"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("DigitalGoodsLicense: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))
