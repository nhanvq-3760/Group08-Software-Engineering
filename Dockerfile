FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-tk \
    tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD ["python3", "Authentication/main.py"]
