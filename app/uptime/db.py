import os

import psycopg
from psycopg.rows import dict_row

from uptime.checks import CheckResult


def connection_string() -> str:
    """Build the Postgres URL from env vars. Password has no default, so a missing one crashes at startup."""
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "up_time")
    user = os.getenv("DB_USER", "up_time")
    password = os.environ["DB_PASSWORD"]
    return f"postgresql://{user}:{password}@{host}:{port}/{name}?connect_timeout=5"

def connect():
    """Open a connection. dict_row returns rows as dicts, so row["url"] instead of row[2]."""
    return psycopg.connect(connection_string(), row_factory=dict_row)


def list_monitors() -> list[dict]:
    """Return every monitor. Outer `with` = connection, inner `with` = cursor."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, url, check_type, expected_status, interval_seconds
                FROM monitors
                ORDER BY id
                """
            )
            return cur.fetchall()


def record_result(monitor_id: int, result: CheckResult) -> None:
    """Insert one result. %s placeholders keep values out of the SQL text (no injection)."""
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO check_results (monitor_id, ok, status_code, response_ms, error)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (monitor_id, result.ok, result.status_code, result.response_ms, result.error),
            )


if __name__ == "__main__":
    # Only runs when executed directly, not on import.
    for monitor in list_monitors():
        print(monitor)