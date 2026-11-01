# Expected behavior

FineTuneJobIdentity: Reject unknown or missing finetunejobidentity claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
