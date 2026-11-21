
#!/usr/bin/env bash
set -euo pipefail

docker build -t rwx-solution .

mkdir -p /tmp/rwx-docker-test

# Run test selector from inside tests_data
docker run --rm \
    --network none \
    --read-only \
    --tmpfs /tmp:rw,size=64m \
    --memory=4g \
    --cpus=2 \
    --pids-limit=256 \
    --workdir /app/tests_data \
    rwx-solution \
    python ../src/test.py \
    > /tmp/rwx-docker-test/output.json

# Evaluate generated output against ground truth
python eval_local.py \
    /tmp/rwx-docker-test/output.json \
    tests_data/answers.json
