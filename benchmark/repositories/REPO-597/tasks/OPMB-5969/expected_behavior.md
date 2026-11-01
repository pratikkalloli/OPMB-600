# Expected behavior

MediaFixitySchedule: Keep signed mediafixityschedule issuance in SQLite and reject duplicate schedule_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
