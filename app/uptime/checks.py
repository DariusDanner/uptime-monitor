import socket
import time
from dataclasses import dataclass
from urllib.parse import urlparse

import httpx

TIMEOUT_SECONDS = 10.0


@dataclass
class CheckResult:
    ok: bool
    status_code: int | None
    response_ms: int | None
    error: str | None = None


def check_http(url: str, expected_status: int = 200) -> CheckResult:
    """Full check: did the service return the status code we expect?"""
    start = time.perf_counter()
    try:
        response = httpx.get(url, timeout=TIMEOUT_SECONDS, follow_redirects=True)
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return CheckResult(
            ok=response.status_code == expected_status,
            status_code=response.status_code,
            response_ms=elapsed_ms,
        )
    except httpx.RequestError as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return CheckResult(False, None, elapsed_ms, error=type(exc).__name__)


def check_tcp(url: str, **_) -> CheckResult:
    """Lenient check: is anything listening on the port at all?"""
    parsed = urlparse(url)
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    start = time.perf_counter()
    try:
        with socket.create_connection((parsed.hostname, port), TIMEOUT_SECONDS):
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            return CheckResult(True, None, elapsed_ms)
    except OSError as exc:
        elapsed_ms = int((time.perf_counter() - start) * 1000)
        return CheckResult(False, None, elapsed_ms, error=type(exc).__name__)


CHECKERS = {"http": check_http, "tcp": check_tcp}