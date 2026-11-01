# Expected behavior

ArtworkCustodyTransfer: Keep signed artworkcustodytransfer issuance in SQLite and reject duplicate transfer_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
