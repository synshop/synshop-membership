FROM docker.io/library/python:3.11-alpine AS builder

RUN pip3 install pipenv
WORKDIR /srv
COPY Pipfile* ./
ENV PIPENV_VENV_IN_PROJECT=1 PYTHONPYCACHEPREFIX=/tmp/pycache
RUN pipenv install --deploy

FROM docker.io/library/python:3.11-alpine AS runner
COPY --from=builder /srv/.venv /srv/.venv
WORKDIR /srv
COPY src ./

EXPOSE 8080

# Nobody user
USER 65532:65532
# We like read-only filesystems
ENV PYTHONPYCACHEPREFIX=/tmp/pycache

ENTRYPOINT ["/srv/.venv/bin/python3", "app.py"]

