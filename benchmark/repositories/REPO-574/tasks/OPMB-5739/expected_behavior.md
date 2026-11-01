# Expected behavior

LongTermDataTombstone: Keep signed longtermdatatombstone issuance in SQLite and reject duplicate tombstone_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
