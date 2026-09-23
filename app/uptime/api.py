import os

from fastapi import FastAPI

from uptime.db import connect

app = FastAPI(title="uptime-monitor")

HISTORY_LIMIT = int(os.getenv("HISTORY_LIMIT", "30"))


@app.get("/healthz")
def healthz():
    """Liveness probe: is the process up?"""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Readiness probe: can we actually reach the database?"""
    try:
        with connect() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not ready"}, 503


@app.get("/api/status")
def status():
    """Every monitor with its recent history, newest first."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, url, check_type FROM monitors ORDER BY id")
            monitors = cur.fetchall()

            for monitor in monitors:
                cur.execute(
                    """
                    SELECT checked_at, ok, status_code, response_ms, error
                    FROM check_results
                    WHERE monitor_id = %s
                    ORDER BY checked_at DESC
                    LIMIT %s
                    """,
                    (monitor["id"], HISTORY_LIMIT),
                )
                results = cur.fetchall()
                monitor["results"] = results
                monitor["current"] = results[0] if results else None

    return {"monitors": monitors}