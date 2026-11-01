# Expected behavior

BuildFarmKeyRotation: Reject unknown or missing buildfarmkeyrotation claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
