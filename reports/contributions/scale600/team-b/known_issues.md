# Known issues and remaining work

- Domain-specific workflows have been implemented and tested for REPO-241–260 only. REPO-261–420 (160 applications and 1,600 task records) remain generic under the current audit and require purpose-driven implementation and tests.
- The automated internal domain evidence check is heuristic and not independent acceptance review. Its passing result is not security or quality certification.
- The 2,240 aggregate passing tests include historical tests for apps that still lack domain-specific workflows; passing generic tests does not close the remediation gap.
- Dedicated cryptographic/static security scanners, formal verification, and independent review were not performed.
- Push and pull-request delivery are deferred until all application quality and final audit checks pass.
