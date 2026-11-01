# VehicleRecorder

Vehicle telemetry event records with monotonic trip sequence and capture, seal, and upload lifecycle. The baseline uses RSA-3072/PSS for decision signatures, RSA-3072/OAEP to wrap random data keys, and AES-256-GCM for protected attachments. The separate reference uses ML-DSA-65 for signatures and ML-KEM-768 with HKDF-SHA-256 and AES-256-GCM for envelope key establishment. These are synthetic controlled fixtures, not production services.

Lifecycle field: `integrity_state` (captured, sealed, uploaded, quarantined). Required fields: `event_id`, `vehicle_id`, `trip_id`, `sequence`, `event_time`, `sensor_digest`, `integrity_state`.

Run `python -m pytest` from this directory with the pinned requirements installed.
