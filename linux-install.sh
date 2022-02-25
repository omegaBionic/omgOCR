#!/bin/bash


# Install python requirements
pip3 install -r requirements.txt

# Install linux requirements
sudo apt-get install libhdf5-dev libhdf5-serial-dev libjasper-dev libqtgui4 libqt4-test tesseract-ocr

# Add french configuration for tesseract
echo "$ sudo cp res/tessdata/fra.traineddata /usr/share/tesseract-ocr/4.00/tessdata/"
sudo cp res/tessdata/fra.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
