FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY ethnidata/ ethnidata/

RUN pip install --no-cache-dir .

HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "from ethnidata import EthniData; EthniData()" || exit 1

CMD ["python", "-c", "from ethnidata import EthniData; ed = EthniData(); print(ed.get_stats())"]
