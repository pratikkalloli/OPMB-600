# Application catalogue

The canonical repository manifest currently lists 17 original, controlled applications. Each has ten candidate migration tasks (170 total). Only the test statuses below are recorded as passed; all other application and reference test statuses remain pending.

| Repository | Application | Domain | Purpose | Tasks | Original tests | Reference tests |
|---|---|---|---|---:|---|---|
| REPO-001 | SecureVault | secure file storage | Local SQLite document vault with per-object authenticated encryption and signed integrity metadata. | 10 | passed | passed |
| REPO-002 | KeyLedger | key management | SQLite inventory for synthetic cryptographic key ownership, expiry, rotation, revocation, and signed lifecycle events. | 10 | passed | passed |
| REPO-003 | SecurePrint | secure print release | Simulation of protected print-job submission, printer-bound encryption, authenticated metadata, controlled release, and cancellation. | 10 | pending | pending |
| REPO-004 | TrustBridge | service identity | Service identity enrollment, certificate issuance simulation, and signed trust updates. | 10 | pending | pending |
| REPO-005 | FleetUpdate | secure firmware updates | Signed firmware release manifests, staged rollout approvals, and device acknowledgements. | 10 | pending | pending |
| REPO-006 | CareLink | healthcare messaging | Confidential clinical message exchange with recipient key establishment and audit signatures. | 10 | pending | pending |
| REPO-007 | PayRoute | payment routing | Synthetic payment instruction signing, recipient key delivery, and idempotent settlement records. | 10 | pending | pending |
| REPO-008 | CodeSignHub | software supply chain | Artifact provenance attestations, release signing, and verification policy. | 10 | pending | pending |
| REPO-009 | EdgeTunnel | secure networking | Gateway session establishment, peer authentication, and protected telemetry envelopes. | 10 | pending | pending |
| REPO-010 | ArchiveSeal | records archiving | Long-retention record sealing, signed indexes, and key rotation metadata. | 10 | pending | pending |
| REPO-011 | DevicePair | iot device enrollment | Manufacturing-time device enrollment, ownership transfer, and signed configuration delivery. | 10 | pending | pending |
| REPO-012 | BuildRelay | ci cd security | CI worker identity, encrypted secret handoff, and signed build attestations. | 10 | pending | pending |
| REPO-013 | CaseExchange | legal document exchange | Matter-scoped document exchange, recipient access, and signed custody events. | 10 | pending | pending |
| REPO-014 | SensorMesh | industrial telemetry | Authenticated sensor batches, gateway verification, and fleet key lifecycle. | 10 | pending | pending |
| REPO-015 | IdentityCache | identity federation | Federated assertion signing, verifier key distribution, and rollover behavior. | 10 | pending | pending |
| REPO-016 | BackupRelay | backup replication | Encrypted backup chunk transfer, replica authentication, and restore integrity. | 10 | pending | pending |
| REPO-017 | PolicyGate | access control | Signed policy bundles, delegated approval, and auditable authorization decisions. | 10 | pending | pending |

All tasks remain candidates pending independent review. The 43 remaining applications and 430 tasks are part of the 60/600 benchmark target and are not present in this inventory.
