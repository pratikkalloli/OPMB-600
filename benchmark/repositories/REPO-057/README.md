# SecureCalendar

SecureCalendar manages synthetic calendars, participants, invitations, event updates, and cancellations. Invitations are signed by the host and event details are encrypted to the participant. Participant verification checks the host signature and invitation version.

## Run the test suites

Install the pinned dependencies with `python -m pip install -r requirements.txt`. Run the classical application tests with `python -m pytest tests/test_securecalendar.py -q`. To run the separate PQC reference tests, set `PYTHONPATH` to `migrated_reference` and run `python -m pytest tests/test_securecalendar_pqc.py -q`. The reference uses ML-KEM-768, ML-DSA-65, HKDF-SHA-256, and AES-GCM where the workflow requires key establishment and protected data. All sample data is fictional.
