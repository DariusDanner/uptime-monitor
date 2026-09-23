import logging
import os
import signal
import time

from uptime.checks import CHECKERS
from uptime.db import list_monitors, record_result

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("worker")

LOOP_INTERVAL = int(os.getenv("LOOP_INTERVAL_SECONDS", "60"))

running = True


def handle_shutdown(signum, frame):
    """Set the flag so the loop exits after the current pass."""
    global running
    log.info("shutdown signal received, finishing current pass")
    running = False


def run_once() -> None:
    """Check every monitor once. One bad monitor must not stop the others."""
    for monitor in list_monitors():
        try:
            checker = CHECKERS[monitor["check_type"]]
            result = checker(monitor["url"], expected_status=monitor["expected_status"])
            record_result(monitor["id"], result)
            log.info(
                "%s ok=%s status=%s %sms",
                monitor["name"], result.ok, result.status_code, result.response_ms,
            )
        except Exception:
            log.exception("check failed for monitor %s", monitor["id"])


def main() -> None:
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    log.info("worker started, interval=%ss", LOOP_INTERVAL)
    while running:
        try:
            run_once()
        except Exception:
            log.exception("pass failed entirely")

        # Sleep in 1s slices so a shutdown signal is noticed quickly.
        for _ in range(LOOP_INTERVAL):
            if not running:
                break
            time.sleep(1)

    log.info("worker stopped")


if __name__ == "__main__":
    main()