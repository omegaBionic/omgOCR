#!/bin/bash

echo "*** Run generate-doc ***"

# Define vars
BUILD_FILE="build"

# Define env vars
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"

# Create build file
mkdir -p $BUILD_FILE

# Move into build file
cd $BUILD_FILE

# CP src
cp ../../src/*.py .

# Generate doc
SOURCE_FILES_LIST=$(ls ../../src/*.py)
for FILE in $SOURCE_FILES_LIST
do
  pydoc3 -w $FILE
done

# Return into root doc directory
cd -

# Create opt
mkdir -p opt

# CP output file into opt
cp build/*.html opt

echo "*** This is the end. ***"
