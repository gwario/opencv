# Polygonerkennung

## Requirements
* Python 2.7
* OpenCV 3.2.0
* Unix based OS

## Usage

`python2 pylondetect.py [--actual /path/to/actual.txt] /path/to/image/dir`

This will create a directory to which all images with pylons will be saved.
The pylons are indicated by rectangles.
Also, a file called results.txt will be generated containing all file names and the top left coordinate of it's pylons.

## Ressources
https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_tutorials.html
