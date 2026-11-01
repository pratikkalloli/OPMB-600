# Expected behavior

PromptTemplateRelease: Keep signed prompttemplaterelease issuance in SQLite and reject duplicate template_id records. Valid signed records remain verifiable; malformed, altered, wrong-key, or inactive records are rejected.
