"""Smoke tests for the benchmark metadata validation commands."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_manifest_files_are_valid_json():
    for name in ("repositories.json","tasks.json"):
        json.loads((ROOT/"benchmark/manifests"/name).read_text(encoding="utf-8"))
def test_task_and_repository_validation_commands_run():
    for module in ("validation.validate_metadata","validation.validate_tasks","validation.validate_repositories","validation.validate_reference_solutions"):
        result=subprocess.run([sys.executable,"-m",module],cwd=ROOT,text=True,capture_output=True)
        assert result.returncode==0, result.stdout+result.stderr
