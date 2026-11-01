# OPMB-600 ? Original PQC Migration Benchmark

OPMB-600 is a research benchmark for studying post-quantum cryptography migration in original, team-created controlled software applications. It is not a collection of independently gathered production repositories.

## Research question

How do migration agents perform when replacing classical public-key cryptography in realistic application workflows, and how do retrieval strategies affect correctness, compatibility, and verification?

## Intended design

The benchmark currently contains 17 original, controlled applications and 170 candidate tasks across 17 application domains. Ten tasks are linked to each application. REPO-001 SecureVault, REPO-002 KeyLedger, and REPO-003 SecurePrint have executable reference migration suites with recorded results. REPO-004 through REPO-017 still have pending reference implementations and skipped placeholder tests (140 task references). No task is accepted yet. The full benchmark target is 60 applications and 600 tasks, leaving 43 applications and 430 tasks to complete. Task families cover RSA signatures, RSA encryption/key-wrapping redesign, key establishment, key management, API and dependency compatibility, and cross-component changes. Reference targets follow NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), or FIPS 205 (SLH-DSA) where supported. See `docs/application_catalogue.md` and `reports/progress.md` for current scope and validation state.

## Setup

Use Python 3.11 or newer:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

On Windows activate with `.venv\Scripts\Activate.ps1`.

## Validation

```sh
python -m validation.run_all
pytest
```

For in-progress batch checks, use `python -m validation.run_all --allow-incomplete`. The default command returns failure until the full 60-repository, 600-task, 600-accepted target is met.

## Research conditions

`experiments/C0` through `C3` describe no-memory, raw-trajectory, reflection, and structured-strategy conditions. Strategies must cite verified source tasks; no outcomes are inferred. Repository-level splits keep projects together.

## Limitations

This foundation does not claim that the 60-project dataset, reference migrations, or held-out evaluations are complete. The validation report treats absent projects and unverified solutions as pending. Classical algorithms in benchmark applications are intentionally insecure examples for migration research and must not be used for production. See `docs/limitations.md`.
