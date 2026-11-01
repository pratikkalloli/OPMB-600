# Expected behavior

UpdateChannelManifest: Reject unknown or missing updatechannelmanifest claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
