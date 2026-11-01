# OPMB-0406: VehicleRecorder: Seal a protected domain attachment

Replace RSA-OAEP data-key wrapping with ML-KEM-derived wrapping keys and AES-GCM, bound to the entity identifier. VehicleRecorder workflow: Vehicle telemetry event records with monotonic trip sequence and capture, seal, and upload lifecycle. Domain-specific invariants: Vehicle events require a nonnegative sequence and a SHA-256 sensor digest. The task concerns fields event_id, vehicle_id, trip_id, sequence, event_time, sensor_digest, integrity_state and legal transitions captured -> sealed -> uploaded -> quarantined.

## Required changes

- Migrate the identified operation to ML-KEM-768 + HKDF-SHA-256 + AES-GCM.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
