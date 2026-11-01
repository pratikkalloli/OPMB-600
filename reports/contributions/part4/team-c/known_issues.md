# Team C known issues

- REPO-060 and OPMB-0591 through OPMB-0600 remain unimplemented.
- EventPass offline revocation depends on verifier snapshot freshness.
- ShipmentProof is a synthetic custody simulation, not legal chain-of-custody evidence.
- DistributedCache, ClearingDesk, and FirmwareFleet model synthetic workflows only; they are not production distributed systems, payment processors, secure boot systems, clinical/legal consent services, production communications services, certified telemetry ingestion systems, production identity and policy services, enterprise backup/recovery guarantees, or tamper-resistant local license enforcement.
- All tasks remain candidates pending integration and independent review.
- The fetched base has 17 global applications / 170 tasks; this branch intentionally leaves shared manifests untouched.
