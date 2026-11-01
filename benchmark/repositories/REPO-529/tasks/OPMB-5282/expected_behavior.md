# Expected behavior

VideoTranscodeManifest: Reject unknown or missing videotranscodemanifest claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
