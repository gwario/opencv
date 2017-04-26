#!/usr/bin/env python

'''
This program detects pylons within images.

Authors: Mario Gastegger, Felix Meiners



usage: pylondetect.py [-h] [--verify] Path

--verify:   Compares the number of detected pylons in an image with the actual number of pylons.
            The actual number of pylons is read from path/actual.txt
            The format of actual.txt is as follows:
                * One file per line
                * <path/to/file>;<#pylons>

Path:       The path to the image files.
'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np


class PylonImage:
    """
    This class represents a pylon image.
    It contains information on the number and position of pylons
    """

    __filename__ = ""
    __image__ = None
    __actual_count__ = 0
    __supposed_count__ = 0

    def __init__(self, filename, actual_count):

        if filename != "":
            self.__filename__ = filename

        if actual_count >= 0:
            self.__actual_count__ = actual_count
        else:
            raise ValueError("Actual pylon count must be greater or equal to zero.")

        image = cv2.imread(self.__filename__)
        if image is not None:
            self.__image__ = image
        else:
            raise ValueError("Invalid file.")

    def get_image(self):
        return self.__image__


def load_actual_count(path):
    """ Returns a dictionary of { filename: actual count, ... } """

    name_count = {}

    with open(os.path.join(path,'actual.txt'), 'r') as actual_file:
        for line_no, line in enumerate(actual_file):
            line_parts = line.split(';')

            if len(line_parts) == 2:
                name_count[line_parts[0]] = int(line_parts[1].strip())
            else:
                raise SyntaxError('Format error in line %d!' % line_no)

    return name_count


def pylon_images_from_folder(path):
    """ Returns a list of PylonImages """

    pylon_images = []

    actual_counts = load_actual_count(path)

    for filename in os.listdir(path):

        if filename.endswith(".png"):
            try:
                pylon_images.append(PylonImage(os.path.join(path, filename), actual_counts[filename]))
            except (ValueError, SyntaxError):
                print ("Failed to create PylonImage from %s" % filename)
        else:
            print('Skipping ', filename)

    print(len(pylon_images), ' PylonImages create.')

    return pylon_images


if __name__ == '__main__':

    import sys, os, argparse

    parser = argparse.ArgumentParser(description='This program detects pylons within images.')
    parser.add_argument('--verify', action='store_const', const=True, help='''Compares the number of detected pylons in an image with the actual number of pylons.
        The actual number of pylons is read from path/actual.txt, which contains one file per line.
        The filename and the number of pylons is separated by a semicolon.''')
    parser.add_argument('Path', nargs=1, help='The path to the image files.')

    args = parser.parse_args()

    path = args.Path[0]

    if not os.path.exists(path) or not os.path.isdir(path):

        print("Path does not exist!")
        sys.exit(1)

    print('Creating PylonImages...')

    pylon_images = pylon_images_from_folder(path)

    print(pylon_images)

    # TODO iterate over files and detect and store result in list

    if args.verify:

        # TODO read verify file
        name_actual_count = load_actual_count(path)

        # TODO show success rate and print detection errors

    else:

        print('result')
        # TODO show results