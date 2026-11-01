# Team A implementation report

## Delivery

- 15 domain-specific application projects completed.
- 150 task definitions created for OPMB-0171 through OPMB-0320.
- 150 original application tests and 150 PQC reference tests passed.
- Every task remains a candidate; no task is accepted.

## Batch results

| Batch | Repositories | Original tests | PQC tests |
|---|---|---:|---:|
| A1 | REPO-018–REPO-022 | 50 passed | 50 passed |
| A2 | REPO-023–REPO-027 | 50 passed | 50 passed |
| A3 | REPO-028–REPO-032 | 50 passed | 50 passed |

## Evidence and limitations

Per-repository commands, raw pytest output, exit codes, counts, environment, and timestamps are stored under `reports/evidence/REPO-018` through `REPO-032`. Source-to-test links are listed in `task_inventory.csv`. The applications are controlled synthetic simulations; their SQLite ledgers and in-memory key registries are not production key custody or deployment systems.
