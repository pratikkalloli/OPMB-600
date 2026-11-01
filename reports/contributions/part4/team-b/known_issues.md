# Team B known issues

- A Codex-managed Python 3.12.14 runtime is available, and `.venv` was created inside this checkout. Installing the pinned requirements failed while downloading `cryptography==50.0.2` from `files.pythonhosted.org:443` with a read timeout; the venv contains only pip. All 30 application suites and Python validators remain NOT RUN.
- Package-source audit found no configured internal pip index or `find-links` source, no pip source environment settings, and no cached wheels in the pip cache or searched repository wheelhouse locations. Do not retry until HTTPS wheel access to `files.pythonhosted.org:443` is permitted or an approved internal index/offline wheelhouse is provided.
- An earlier user-scoped Python 3.13.17 installer attempt was rejected: its SHA-256 did not match Python.org's published release checksum and setup returned Windows error 1392. That artifact was removed and was not reused.
- Team B manifests have NOT been validated against the repository's Draft 2020-12 JSON Schemas. The pinned `jsonschema==4.25.1` dependency could not be installed; no compatible Node schema validator is present.
- WSL enumeration returned access denied; Docker is unavailable; no approved pre-provisioned runtime was found. No packages were installed.
- No test result, scanner output, cryptographic verification result, or accepted status is claimed.
- GitHub fetch failed because github.com:443 is unreachable; the local base ref is 31d9fc3fb9767966100209305d9b78c487a6de24. Push and PR creation are blocked.
- Global manifests, shared schemas, documentation, splits, and validation scripts are intentionally unchanged; integration belongs to the integration owner.
- Split assignment, independent review, security review, and production suitability remain outstanding.
