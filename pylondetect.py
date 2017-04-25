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

'''
Returns a dictionary of { filename: cv2.imread, ... }
'''
def load_images_from_folder(path):

    images = {}

    for filename in os.listdir(path):

        if filename.endswith(".png"):

            img = cv2.imread(os.path.join(path,filename))

            if img is not None:
                images[filename] = img
            else:
                print('Failed to load image file:', filename)
                sys.exit(1)

        else:
            print('Skipping ', filename)

    print(len(images), 'loaded.')

    return images


'''
Returns a dictionary of { filename: actual count, ... }
'''
def load_actual_count(path):

    actual = {}

    # TODO iterate over os.path.join(path,'actual.txt')

    # TODO add to actual

    print('actual pylons')

    return actual



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

    print('Loading images...')

    name_im = load_images_from_folder(path)

    # TODO iterate over files and detect and store result in list

    if args.verify:

        # TODO read verify file
        name_actual_count = load_actual_count(path)

        # TODO show success rate and print detection errors

    else:

        print('result')
        # TODO show results