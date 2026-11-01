# SecurePrint

A local simulation of protected print release. It registers fictional users and printers, encrypts submitted job bytes with AES-256-GCM under a fresh data key, wraps that key for an authorized printer using RSA-OAEP, signs job metadata using RSA-PSS, and keeps an auditable in-memory job state. It is not a printer driver or production service.

## Run

From this directory, install `requirements.txt`, then run `python -m pytest`. Import with `PYTHONPATH=src python -c "from secureprint.service import PrintService"`.

The `migrated_reference/secureprint_pqc` package is an isolated reference using ML-KEM-768 for key encapsulation, HKDF-SHA-256, AES-GCM, and ML-DSA-65 for manifests. It requires the pinned `cryptography==50.0.2` APIs. The original and reference use incompatible key and signature encodings by design; there is no implicit classical fallback.

Only synthetic identities and documents should be used. Keys in this in-memory example are generated at process startup and are not durable or hardware protected.
