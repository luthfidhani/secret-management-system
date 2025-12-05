FROM python:3.11-slim-bullseye
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /bin/uv

ENV PYTHONUNBUFFERED=True \
    APP_HOME=/app \
    PORT=5000 \
    UV_PROJECT_ENVIRONMENT="/opt/.venv" \
    PATH="/opt/.venv/bin:$PATH"

WORKDIR $APP_HOME
COPY . ./

RUN uv sync --frozen --no-cache

EXPOSE 5000

CMD exec gunicorn --bind 0.0.0.0:$PORT --timeout 300 app:app