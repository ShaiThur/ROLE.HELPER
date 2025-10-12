FROM library/python:3.13 AS builder

WORKDIR /app

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir \
      -r requirements.txt

COPY sql/ ./sql
COPY app/ ./
COPY .env ./

FROM library/python:3.13 AS final
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY --from=builder /app /app

CMD ["python", "main.py"]