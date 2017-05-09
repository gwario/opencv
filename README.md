# Polygonerkennung

## Requirements
* Python 2.7
* OpenCV 3.2.0
* Unix based OS

## Usage

usage: pylondetect.py [-h] [--actual ACTUAL] --method METHOD [--debug]
                      imagePath

This program detects pylons within images.

positional arguments:
  imagePath        The path to the image files.

optional arguments:
  -h, --help       show this help message and exit
  --actual ACTUAL  Compares the number of detected pylons in an image with the
                   actual number of pylons. The actual number of pylons is
                   read from the file <ACTUAL>, which contains one file per
                   line. The filename and the number of pylons is separated by
                   a semicolon.
  --method METHOD  "color" for the color scanning + color transition state
                   machine (takes three times longer but performs much better)
                   "template" for the template matching.
  --debug          Prints to stdout and writes the images, with matches
                   marked, to the results directory

## Ressources
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html
