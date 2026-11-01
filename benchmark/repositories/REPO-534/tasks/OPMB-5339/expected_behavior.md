# Expected behavior

AudiobookChapterSeal: Keep signed audiobookchapterseal issuance in SQLite and reject duplicate seal_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
