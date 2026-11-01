# Expected behavior

Migrate WorkcellRecipeVault canonicalize the complete domain record for signing from RSA-3072 PSS/SHA-256 to ML-DSA-65, retaining Recipe authoring, quality review, controlled release, and retirement for one manufacturing workcell. semantics.

Valid workcell recipe operations remain interoperable with the documented PQC format. Invalid state, bad recipe_digest, altered content, wrong keys, and unsupported versions are rejected.
