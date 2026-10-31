"""Run all benchmark metadata checks and emit a quality report."""
import subprocess,sys
checks=["validate_metadata","validate_tasks","detect_duplicates","validate_repositories","validate_reference_solutions"]
failed=False
for module in checks:
 print(f"\n== {module} ==",flush=True)
 result=subprocess.run([sys.executable,"-m",f"validation.{module}"])
 failed |= result.returncode != 0
print("\n== quality report ==",flush=True)
result=subprocess.run([sys.executable,"-m","validation.generate_quality_report"])
failed |= result.returncode != 0
raise SystemExit(1 if failed else 0)
