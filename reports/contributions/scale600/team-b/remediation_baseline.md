# Remediation inventory — current checkpoint

Inspected 180 assigned applications from the actual service, domain, test and concept files.

- Normalized service implementation shapes: 31.
- Applications whose service exposes only the shared `register` / `retrieve` / `approve` / `verify_approval` / `advance` record API: 150.
- Applications already exposing specialized service operations: 30.
- Normalized test module shapes: 180.
- Domain validator modules differ in rule expression/configuration, but this alone does not establish the README-described workflow.
- All assigned IDs, concepts, service methods, domain functions, and test function names are enumerated in `remediation_inventory.csv`.

This is a current inventory, not a final acceptance audit. No application is considered domain-specific solely because its title, field, rule value, enum, or lifecycle label differs. The separately maintained domain audit records workflow tests and specialized service behavior.
