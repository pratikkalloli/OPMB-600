# Expected behavior

- Authorization is allowed only for the matching subject, study, permitted scope, and unexpired active grant.
- Revocation blocks subsequent access checks and retains its reason and timestamp.
- Consent identity, revision, and expiry are protected by the authority signature.
