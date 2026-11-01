# BackupVault

BackupVault stores synthetic encrypted backup snapshots by owner and monotonically increasing generation. A signed manifest binds the snapshot identifier, owner, generation, and ciphertext digest. Restore checks the owner, signer, and generation state. The baseline uses RSA-PSS and X25519; the reference uses ML-DSA-65 and ML-KEM-768 with HKDF-SHA-256 and AES-GCM.
