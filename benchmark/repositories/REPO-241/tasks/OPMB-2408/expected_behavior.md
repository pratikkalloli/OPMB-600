# Expected behavior

Migrate WorkcellRecipeVault protect a workflow artifact for an authorized recipient from RSA-3072 OAEP/SHA-256 with AES-256-GCM to ML-KEM-768 and AES-256-GCM, retaining Recipe authoring, quality review, controlled release, and retirement for one manufacturing workcell. semantics.

Valid workcell recipe operations remain interoperable with the documented PQC format. Invalid state, bad recipe_digest, altered content, wrong keys, and unsupported versions are rejected.
