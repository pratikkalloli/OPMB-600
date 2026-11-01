# OPMB-0408: VehicleRecorder: Encode recipient public-key material

Replace RSA PEM serialization with the pinned provider raw ML-KEM-768 public-key encoding and update consumers. VehicleRecorder workflow: Vehicle telemetry event records with monotonic trip sequence and capture, seal, and upload lifecycle. Domain-specific invariants: Vehicle events require a nonnegative sequence and a SHA-256 sensor digest. The task concerns fields event_id, vehicle_id, trip_id, sequence, event_time, sensor_digest, integrity_state and legal transitions captured -> sealed -> uploaded -> quarantined.

## Required changes

- Migrate the identified operation to ML-KEM-768.
- Preserve the domain workflow and update dependent callers or serialized keys.
- Keep signing, key establishment, key derivation, and payload encryption distinct.
