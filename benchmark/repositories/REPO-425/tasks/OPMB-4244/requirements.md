# Migration requirements

modified key digest invalidates the transition signature. Preserve tenant_key_rotation_registry semantics. Use ML-DSA-65 with versioned key serialization and no classical fallback.
