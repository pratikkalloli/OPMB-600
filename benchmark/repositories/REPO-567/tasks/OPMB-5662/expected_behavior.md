# Expected behavior

AvailabilityStatusSeal: Reject unknown or missing availabilitystatusseal claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
