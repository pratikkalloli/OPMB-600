# Integration notes

- Integrate the 15 repository records and 150 task records from these contribution manifests only through the designated integration owner.
- No shared schemas, root docs, global indexes, reports, splits, validation scripts, or other application directories were changed.
- Current permissive schemas support the metadata fields used; no schema extension is proposed.
- Applications pin cryptography==50.0.2 and pytest==8.4.2, matching project dependencies.
- Run batch tests and shared validators in an approved Python 3.11+ environment. Put actual output under reports/evidence/REPO-XXX before updating any validation status.
- Assign dataset splits globally after repository grouping and leakage review. Do not mark tasks accepted based on file presence.
