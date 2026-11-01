# Expected behavior

- Published records have deterministic canonical bytes and valid signatures.
- Zone serials increase monotonically; revoked zones cannot be published or transferred.
- Resolvers reject snapshots with mismatched signature keys or altered contents.
