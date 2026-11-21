#!/usr/bin/env bash
set -euo pipefail

docker build -t rwx-solution .

OUTPUT_DIR="/tmp/rwx-docker-test"

mkdir -p "$OUTPUT_DIR"
chmod 777 "$OUTPUT_DIR"

docker run --rm \
    --network none \
    --read-only \
    --tmpfs /tmp:rw,size=64m \
    --memory=4g \
    --cpus=2 \
    --pids-limit=256 \
    --workdir /app/tests_data \
    --mount "type=bind,source=$OUTPUT_DIR,target=/output" \
    -e output_file_path=/output/output.json \
    rwx-solution \
    python ../src/test.py

python eval_local.py \
    "$OUTPUT_DIR/output.json" \
    tests_data/answers.json
