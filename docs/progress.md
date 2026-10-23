# Progress

## 2026-10-23
- Recreated kind cluster `uptime` (config now in repo: kind-config.yaml)
- Fixed /readyz returning 200 instead of 503
- Phase 2 done: API, worker, Postgres (StatefulSet + PVC + schema ConfigMap), Secret, Services
- ArgoCD installed on kind, app synced from k8s/, auto-sync + selfHeal + prune tested
- Gotcha: VPN on = kubectl TLS handshake timeout against kind

## Known issues
- Worker ignores SIGTERM during sleep(60) -> killed after 30s grace period
- Multiple worker replicas = duplicate checks (worker is not built for >1 replica)
- DB password in Git (local dummy only)

## Next
- Scale worker back to 1 (via Git)
- Kyverno on kind: Restricted policies in Audit mode against own app
