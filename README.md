# OPMB-600 ? Original PQC Migration Benchmark

OPMB-600 is a research benchmark for studying post-quantum cryptography migration in original, team-created controlled software applications. It is not a collection of independently gathered production repositories.

## Research question

How do migration agents perform when replacing classical public-key cryptography in realistic application workflows, and how do retrieval strategies affect correctness, compatibility, and verification?

## Intended design

The full benchmark targets 60 distinct applications and 600 tasks across nine application domains. Task families cover RSA signatures, RSA encryption/key wrapping redesign, ECDSA, ECDH, key management, API/dependency compatibility, and cross-component changes. Reference targets follow NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), or FIPS 205 (SLH-DSA) where supported. The current checkout is an initial foundation; see `reports/progress.md` for implemented and pending scope.

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

## Research conditions

`experiments/C0` through `C3` describe no-memory, raw-trajectory, reflection, and structured-strategy conditions. Strategies must cite verified source tasks; no outcomes are inferred. Repository-level splits keep projects together.

## Limitations

This foundation does not claim that the 60-project dataset, reference migrations, or held-out evaluations are complete. The validation report treats absent projects and unverified solutions as pending. Classical algorithms in benchmark applications are intentionally insecure examples for migration research and must not be used for production. See `docs/limitations.md`.
