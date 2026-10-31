"""Run dataset checks. Full acceptance fails until the 60/600 target is met."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main()->int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--allow-incomplete",action="store_true",help="run consistency checks on an in-progress batch without claiming acceptance")
    args=parser.parse_args(); failed=False
    for module in ("validate_metadata","validate_tasks","detect_duplicates","validate_repositories","validate_reference_solutions"):
        print(f"\n== {module} ==",flush=True)
        result=subprocess.run([sys.executable,"-m",f"validation.{module}"],cwd=ROOT)
        failed |= result.returncode!=0
    print("\n== quality report ==",flush=True)
    result=subprocess.run([sys.executable,"-m","validation.generate_quality_report"],cwd=ROOT); failed |= result.returncode!=0
    repos=json.loads((ROOT/"benchmark/manifests/repositories.json").read_text(encoding="utf-8")).get("repositories",[]); tasks=json.loads((ROOT/"benchmark/manifests/tasks.json").read_text(encoding="utf-8")).get("tasks",[])
    incomplete=len(repos)!=60 or len(tasks)!=600 or any(t.get("validation_status")!="accepted" for t in tasks)
    if incomplete and not args.allow_incomplete:
        print("\nACCEPTANCE FAILED: requires 60 repositories, 600 tasks, and 600 accepted tasks. Use --allow-incomplete for batch consistency checks.")
        failed=True
    return int(failed)
if __name__=="__main__": raise SystemExit(main())
