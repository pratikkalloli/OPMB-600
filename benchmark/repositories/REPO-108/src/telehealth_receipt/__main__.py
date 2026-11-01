"""Command-line entry point for TelehealthReceipt."""
import json, sys
from pathlib import Path
from .workflow import create_telehealth_receipt_identity, run_telehealth_receipt_workflow

def main(argv=None) -> int:
    try:
        raw = Path(argv[0]).read_text(encoding="utf-8") if argv else sys.stdin.read()
        result = run_telehealth_receipt_workflow(create_telehealth_receipt_identity(), json.loads(raw))
        print(json.dumps({"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("TelehealthReceipt: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))
