#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

echo "System dependencies installed!"

# Create model directory
mkdir -p ./models

echo "Setup completed successfully!" 