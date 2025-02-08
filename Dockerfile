
FROM python:3.13-slim-bookworm AS base

ARG DEV=false
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=2.0.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

FROM base as dev

WORKDIR /app

COPY project-contributors-api/poetry.lock project-contributors-api/pyproject.toml ./

RUN pip install poetry==${POETRY_VERSION}

RUN if [ $DEV ]; then poetry install --with dev --no-root --no-cache; else poetry install --without dev --no-root --no-cache; fi

COPY scripts/entrypoints/dev-entrypoint.sh .

ENTRYPOINT ["./dev-entrypoint.sh"]

FROM base as prod

RUN useradd -m -r appuser && \
    mkdir /app && \
    chown -R appuser /app

WORKDIR /app

COPY --from=dev ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY --chown=appuser:appuser project-contributors-api .
COPY --chown=appuser:appuser scripts/entrypoints/prod-entrypoint.sh .

USER appuser

ENTRYPOINT ["./prod-entrypoint.sh"]