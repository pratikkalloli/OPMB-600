# Expected behavior

StreamingLicenseGrant: Reject unknown or missing streaminglicensegrant claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
