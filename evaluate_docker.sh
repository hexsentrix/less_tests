#!/usr/bin/env bash
set -euo pipefail

docker build -t rwx-solution .

mkdir -p /tmp/rwx-docker-test

docker run --rm \
    --network none \
    --read-only \
    --tmpfs /tmp:rw,size=64m \
    --memory=4g \
    --cpus=2 \
    --pids-limit=256 \
    --workdir /app/tests_data \
    --mount type=bind,source=/tmp/rwx-docker-test,target=/output \
    -e output_file_path=/output/output.json \
    rwx-solution \
    python ../src/test.py

python eval_local.py \
    /tmp/rwx-docker-test/output.json \
    tests_data/answers.json
