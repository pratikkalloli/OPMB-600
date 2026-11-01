# DistributedCache

DistributedCache simulates encrypted cache-snapshot transfer between registered nodes. The sender establishes a session using X25519 ECDH in the baseline, encrypts a versioned snapshot with AES-GCM, and signs the transfer metadata with ECDSA. The reference uses ML-KEM-768, HKDF-SHA-256, AES-GCM, and ML-DSA-65. Node identifiers and cache payloads are synthetic; this is not a distributed production cache.

Install requirements.txt and run pytest from this directory.
