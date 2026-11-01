"""Command-line entry point for TaxRemit."""
import json, sys
from pathlib import Path
from .workflow import create_tax_remit_identity, run_tax_remit_workflow

def main(argv=None) -> int:
    try:
        raw = Path(argv[0]).read_text(encoding="utf-8") if argv else sys.stdin.read()
        result = run_tax_remit_workflow(create_tax_remit_identity(), json.loads(raw))
        print(json.dumps({"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print("TaxRemit: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__": raise SystemExit(main(sys.argv[1:]))
