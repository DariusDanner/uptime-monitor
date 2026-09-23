# Deliberate shortcuts

Taken to reach the Kubernetes phase sooner. To revisit in phase 7.

- No status page UI — the API returns JSON only
- Per-monitor `interval_seconds` is ignored; the worker uses one global interval
- No tests
- Database credentials are hardcoded in compose.yml (fine locally, becomes a Secret in k8s)
- The API runs one query per monitor; would need rethinking at scale
