-- Monitors: one row per thing being watched.

CREATE TABLE monitors (
    id               BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name             TEXT    NOT NULL,
    url              TEXT    NOT NULL UNIQUE,
    check_type       TEXT    NOT NULL DEFAULT 'http'
                             CHECK (check_type IN ('http', 'tcp')),
    expected_status  INTEGER NOT NULL DEFAULT 200,
    interval_seconds INTEGER NOT NULL DEFAULT 60
                             CHECK (interval_seconds > 0),
    created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- Check results: one row per check performed. Grows forever.

CREATE TABLE check_results (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    monitor_id  BIGINT NOT NULL REFERENCES monitors(id) ON DELETE CASCADE,
    checked_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ok          BOOLEAN NOT NULL,
    status_code INTEGER,
    response_ms INTEGER,
    error       TEXT
);


-- The status page always asks: "latest results for monitor X".
-- Without this, Postgres scans the entire table every time.

CREATE INDEX idx_check_results_monitor_time
    ON check_results (monitor_id, checked_at DESC);