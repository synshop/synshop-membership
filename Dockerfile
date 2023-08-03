FROM docker.io/library/python:3.11-alpine AS builder

RUN pip3 install pipenv
COPY Pipfile* /srv
ENV PIPENV_VENV_IN_PROJECT=1 PYTHONPYCACHEPREFIX=/tmp/pycache
WORKDIR /srv
COPY src .
RUN pipenv install --deploy

FROM docker.io/library/python:3.11-alpine AS runner
COPY --from=builder /srv/.venv /srv/.venv
WORKDIR /srv
COPY src .

EXPOSE 8080

USER nobody:nobody
# We like read-only filesystems
ENV PYTHONPYCACHEPREFIX=/tmp/pycache
CMD ["/srv/.venv/bin/python3", "app.py"]

