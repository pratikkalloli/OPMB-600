# Expected behavior

ModelDistributionTicket: Keep signed modeldistributionticket issuance in SQLite and reject duplicate ticket_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
