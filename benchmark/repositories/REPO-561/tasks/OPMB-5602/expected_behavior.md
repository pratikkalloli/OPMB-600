# Expected behavior

SharedFolderAccessGrant: Reject unknown or missing sharedfolderaccessgrant claim fields before cryptographic processing. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
