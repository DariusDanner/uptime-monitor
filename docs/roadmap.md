# Roadmap

## v1 — in scope

- Monitors defined in the database, inserted via SQL
- Background worker checks each URL on a fixed interval
- Results stored one row per check
- Single status page showing current state and recent history
- Configurable check type per monitor (TCP connect, HTTP status)

## Deliberately deferred

These are understood but intentionally out of scope for v1, to keep the
application small enough that the infrastructure stays the focus.

- Alerting (email, webhook) on state change
- Web UI for adding and editing monitors
- Authentication and multi-tenancy
- Response time graphs over long periods
- Embeddable status badges
- Public status page separate from the admin view
