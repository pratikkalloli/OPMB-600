# Expected behavior

RemoteWorkshopCredential: Reject unknown or missing remoteworkshopcredential claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
