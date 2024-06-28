#!/bin/bash

# Choose a container name for bookkeeping
export CONTAINER_NAME=llama3-8b-instruct

# Choose a LLM NIM Image from NGC
export IMG_NAME="nvcr.io/nim/meta/${CONTAINER_NAME}:1.0.0"

# Choose a path on your system to cache the downloaded models
export LOCAL_NIM_CACHE=~/.cache/nim
mkdir -p "$LOCAL_NIM_CACHE"

# Set NGC_API_KEY to nv_NGC_API_KEY (to differentiate from riva)
export NGC_API_KEY="$nv_NGC_API_KEY"

echo "NGC_API_KEY set to $NGC_API_KEY"
echo "Run with sudo -E ./nim_server.sh so the NGC_API_KEY is retained "

# Start the LLM NIM (modify the GPUs accordingly if u are messing ard with lots of containers )
docker run -d --name=$CONTAINER_NAME \
  --runtime=nvidia \
  --gpus "device=1" \
  --shm-size=16GB \
  -e NGC_API_KEY \
  -v "$LOCAL_NIM_CACHE:/opt/nim/.cache" \
  -u $(id -u) \
  -p 8001:8000 \
  $IMG_NAME

# TODO:
# pause the container, restart the container  (with docker start, docker stop etc.)

