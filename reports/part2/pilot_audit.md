# REPO-001 SecureVault engineering audit

Date: 2026-11-01
Scope: source review of the original and reference cryptographic paths, storage, task mapping, and current test evidence. This is an engineering review, not independent cryptographic certification.

## Findings and actions

1. **High, fixed ? implicit ephemeral signing key.** Both services previously generated a signer when none was supplied. A restarted process could not verify documents signed by the earlier in-memory key. Constructors now require an explicit signing key, making ownership and persistence a caller responsibility instead of silently creating an unusable key. Tests pass a stable key instance.
2. **Medium, fixed ? incomplete manifest binding.** The manifest originally covered object ID, filename, and ciphertext digest but omitted the GCM nonce and wrapped data key. Both implementations now sign hashes of the ciphertext, nonce, and wrapped key plus the object ID and filename. New database-tampering tests confirm nonce/wrapped-key edits fail before decryption.
3. **Medium, open ? key lifecycle remains external.** The service accepts keys from its caller and does not implement durable private-key storage, recovery, or an end-to-end persisted recipient rotation workflow. The reference has a tested isolated rewrap primitive, not a store-wide rotation transaction. Do not reuse this lifecycle design in later projects; each new app must model key storage and rotation explicitly.
4. **Medium, open ? PQC private-key serialization is not covered.** The reference tests ML-KEM public-key raw serialization, but not private-key persistence or restoration, nor ML-DSA key serialization. Tasks claiming broad key serialization must be narrowed or expanded with executable tests before acceptance.
5. **Low, documented ? metadata visibility.** Filenames and object IDs remain plaintext in SQLite. This pilot protects document bytes and integrity metadata, not metadata confidentiality.
6. **Low, documented ? scanner scope.** The lexical scanner checks Python source patterns only; it does not analyze dependencies, runtime-loaded code, data files, or cryptographic side channels.

## Cryptographic path review

- Original payload encryption uses a fresh 32-byte data key, a 96-bit random AES-GCM nonce, and object ID AAD. RSA-3072 OAEP/SHA-256 transports the per-object key. RSA-3072 PSS/SHA-256 signs a canonical manifest. Signing and recipient keys are distinct inputs.
- Reference uses ML-KEM-768 encapsulation; HKDF-SHA-256 derives a key-encryption key with object-specific `info`; AES-GCM wraps the random data key. Payloads remain AES-GCM encrypted with the object ID as AAD. ML-DSA-65 signs the canonical manifest. The ML-KEM ciphertext length follows the pinned library API and the stored format is currently fixed to ML-KEM-768.
- The reference tests matching KEM-derived wrapping/dewrapping, wrong-recipient and modified-context rejection, ML-DSA modified-message and wrong-key rejection, public-key raw serialization, rewrapping, payload tamper rejection, and application round trip.

## Task mapping and evidence

The ten tasks target ten distinct callable operation boundaries. Some are dependent (wrap/unwrap and sign/verify); their independent value is API migration plus direction-specific negative verification. Tasks remain candidates because no independent reviewer has approved the task decomposition or reference patch.

After fixes, original tests: **11 passed**. Reference tests: **9 passed**. No test failures. Evidence: `reports/evidence/REPO-001/test-results.json`.

## Guidance for later applications

Use caller-owned, explicit keys; model persistent key lifecycle; sign all security-relevant stored metadata; exercise private/public serialization when a task claims it; and keep application-specific migration tests separate from primitive unit tests.
