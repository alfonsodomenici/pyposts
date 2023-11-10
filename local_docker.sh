#!/bin/sh
docker build -t pyposts .
docker rm -f pyposts || true && docker run -d -p 5000:5000 \
    --network  db \
    --env-file ./.env.docker.local \
    --name pyposts pyposts 