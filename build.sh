#!/bin/bash

WORKING_DIRECTORY="build"
PROGRAM_NAME="omgOcr"

# Generate project, c and compile
python3 setup.py build_ext --inplace

# Create build file
rm -rf $WORKING_DIRECTORY
mkdir -p $WORKING_DIRECTORY
mv src/*.c src/*.so $WORKING_DIRECTORY