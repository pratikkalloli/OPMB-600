"""Command-line entry point for WebhookShield."""
import argparse
import json
import sys
from pathlib import Path
from .workflow import create_delivery_identity, run_webhookshield_workflow

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate and sign one delivery JSON record")
    parser.add_argument("record", nargs="?", help="JSON file; reads stdin when omitted")
    args = parser.parse_args(argv)
    try:
        raw = Path(args.record).read_text(encoding="utf-8") if args.record else sys.stdin.read()
        record = json.loads(raw)
        result = run_webhookshield_workflow(create_delivery_identity(), record)
        print(json.dumps({"record": result["record"], "signature": result["signature"].decode(), "context": result["context"]}, sort_keys=True))
        return 0
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"WebhookShield: {exc}", file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
