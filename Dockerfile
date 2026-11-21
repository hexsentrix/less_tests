FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOME=/tmp

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY tests_data/ ./tests_data/
COPY assets/ ./assets/
COPY run.sh .

# Set the working directory for the application
WORKDIR /data

USER nobody

CMD ["python", "-u", "/app/src/main.py"]