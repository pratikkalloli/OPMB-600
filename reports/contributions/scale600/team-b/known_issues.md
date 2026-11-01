# Known issues and remaining work

- Domain-specific workflows have been implemented and tested for REPO-241–270 only. REPO-271–420 (150 applications and 1,500 task records) remain generic under the current audit and require purpose-driven implementation and tests.
- The automated internal domain evidence check is heuristic, not independent acceptance review. Its passing result is not security or quality certification.
- The 2,280 aggregate passing tests include historical tests for apps that still lack domain-specific workflows; passing generic tests does not close the remediation gap.
- Dedicated cryptographic/static security scanners, formal verification, and independent review were not performed.
- The current full audit is structurally passed but incomplete. No claim of complete quality or delivery readiness is made.
