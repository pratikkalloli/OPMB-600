# Team C known issues

- All 130 tasks remain candidates pending integration and independent acceptance review.
- EventPass offline revocation depends on the freshness of the verifier's revocation snapshot.
- ShipmentProof, InventoryHandoff, EnergyMeter, TenderProof, and the other domain systems use synthetic records and are not production services.
- RemoteAttestation is a software simulation only; it does not provide hardware-rooted attestation or trusted hardware support.
- Scanner evidence is lexical and does not inspect dependencies, dynamic code, runtime behavior, or serialized artifacts.
- Shared canonical manifests, global catalogue/statistics, schemas, validators, and root progress files are unchanged on this contribution branch.
