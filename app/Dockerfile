# ---- build stage ----
FROM python:3.13-slim AS build

WORKDIR /app

# Install dependencies into a virtualenv we can copy out later.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# ---- runtime stage ----
FROM python:3.13-slim

# Run as a non-root user. Containers default to root, which is a
# needless privilege and something Kyverno-style policies will reject.
RUN useradd --create-home --uid 1000 appuser

WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=build /opt/venv /opt/venv
COPY uptime/ ./uptime/

USER appuser

# Default to the API; the worker overrides this with its own command.
CMD ["uvicorn", "uptime.api:app", "--host", "0.0.0.0", "--port", "8000"]
