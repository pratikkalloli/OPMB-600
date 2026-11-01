# Expected behavior

- Only the matching active owner can restore a backup encrypted to that owner.
- Backup generations increase monotonically and duplicate IDs fail.
- The signed manifest authenticates owner, generation, and ciphertext digest.
