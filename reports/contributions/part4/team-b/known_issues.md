# Team B known issues

- Python and pytest remain unavailable; all 30 application suites and shared validators are NOT RUN. An attempted user-scoped Python 3.13.17 setup could not be trusted: the downloaded installer SHA-256 did not match Python.org's published release checksum, and setup returned Windows error 1392. The installer was removed; no Python runtime or project dependency was installed.
- Team B manifests have NOT been validated against the repository's Draft 2020-12 JSON Schemas. The documented `jsonschema==4.25.1` dependency could not be installed; no compatible Node schema validator is present.
- WSL enumeration returned access denied; Docker is unavailable; no approved pre-provisioned runtime was found. No packages were installed.
- No test result, scanner output, cryptographic verification result, or accepted status is claimed.
- GitHub fetch failed because github.com:443 is unreachable; the local base ref is 31d9fc3fb9767966100209305d9b78c487a6de24. Push and PR creation are blocked.
- Global manifests, shared schemas, documentation, splits, and validation scripts are intentionally unchanged; integration belongs to the integration owner.
- Split assignment, independent review, security review, and production suitability remain outstanding.
