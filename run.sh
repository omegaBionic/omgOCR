#!/bin/bash



# Define env variable
PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

python3 src/core.py
