# Expected behavior

MusicSessionSplitSheet: Keep signed musicsessionsplitsheet issuance in SQLite and reject duplicate sheet_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
