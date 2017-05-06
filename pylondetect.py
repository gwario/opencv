#!/usr/bin/env python

'''
This program detects pylons within images.

Authors: Mario Gastegger, Felix Meiners



usage: pylondetect.py [-h] [--actual Actual] Path

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
    __actual_count__ = None
    __supposed_count__ = None

    def __init__(self, filename, actual_count=None):

        if filename != "":
            self.__filename__ = filename

        if actual_count is not None:
            if actual_count >= 0:
                self.__actual_count__ = actual_count
            else:
                raise ValueError("Actual pylon count must be greater or equal to zero.")

        image = cv2.imread(self.__filename__)
        if image is not None:
            self.__image__ = image
        else:
            raise ValueError("Invalid file.")

    def get_filename(self):
        return self.__filename__

    def get_image(self):
        return self.__image__

    def set_supposed_count(self, count):
        if count >= 0:
            self.__supposed_count__ = count
        else:
            raise ValueError("Pylon count must be greater or equal to zero.")

    def get_supposed_count(self):
        return self.__supposed_count__

    def set_actual_count(self, count):
        if count >= 0:
            self.__actual_count__ = count
        else:
            raise ValueError("Pylon count must be greater or equal to zero.")

    def get_actual_count(self):
        return self.__actual_count__

    def correctly_recognized(self):
        return self.__supposed_count__ is not None and self.__actual_count__  is not None and self.__supposed_count__ == self.__actual_count__


def match_templates(image):
    "Compares image to list of template images and returns the matches"
    numberOfDetections = 0

    for template in os.listdir("templates"):

        if (template.endswith(".png")):
            img_gray = cv2.cvtColor(image.__image__, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(cv2.imread(os.path.join("templates", template)), cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            for pt in zip(*loc[::-1]):
                numberOfDetections += 1
                #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
        else:
            print("Skipping file " + template)

    return numberOfDetections


def load_actual_count(actual_txt_file):
    """ Returns a dictionary of { filename: actual count, ... } """

    name_count = {}

    for line_no, line in enumerate(actual_txt_file):
        line_parts = line.split(';')

        if len(line_parts) == 2:
            name_count[line_parts[0]] = int(line_parts[1].strip())
        else:
            raise SyntaxError('Format error in line %d!' % line_no)

    return name_count


def pylon_images_from_folder(img_dir_path, actual_txt_file):
    """ Returns a list of PylonImages """

    pylon_images = []

    actual_counts = {}
    if actual_txt_file is not None:
        actual_counts = load_actual_count(actual_txt_file)

    for filename in os.listdir(imgDirPath):

        if filename.endswith(".png"):
            try:
                pylonImage = PylonImage(os.path.join(img_dir_path, filename), 0)

                if filename in actual_counts:
                    pylonImage.set_actual_count(actual_counts[filename])

                pylon_images.append(pylonImage)

            except (ValueError, SyntaxError):
                print ("Failed to create PylonImage from %s" % filename)
        else:
            print('Skipping ', filename)

    print(len(pylon_images), 'PylonImages processed.')

    return pylon_images


if __name__ == '__main__':

    import sys, os, argparse

    parser = argparse.ArgumentParser(description='This program detects pylons within images.')
    parser.add_argument('--actual', type=argparse.FileType('r'), help='''Compares the number of detected pylons in an image with the actual number of pylons.
        The actual number of pylons is read from the file <ACTUAL>, which contains one file per line.
        The filename and the number of pylons is separated by a semicolon.''')
    parser.add_argument('imagePath', nargs=1, help='The path to the image files.')

    args = parser.parse_args()

    imgDirPath = args.imagePath[0]
    actualTxtFilePath = args.actual

    print(args)

    if not os.path.exists(imgDirPath) or not os.path.isdir(imgDirPath):

        print("Path to image files does not exist!")
        sys.exit(1)

    print('Processing PylonImages...')

    pylon_images = pylon_images_from_folder(imgDirPath, actualTxtFilePath)

    print('Analyzing...')

    for pylonImage in pylon_images:
        # analyze image
        pylonImage.set_supposed_count(match_templates(pylonImage))
        # write result to stdout TODO implement the required format
        #print(pylonImage.get_filename() + ':', pylonImage.get_supposed_count())

    print('Generating result...')

    # show success rate and print detection errors
    existingPylons = 0
    foundPylons = 0

    for pylonImage in pylon_images:
        foundPylons += pylonImage.get_supposed_count()

        if actualTxtFilePath is not None:
            existingPylons += pylonImage.get_actual_count()

            if pylonImage.correctly_recognized():
                print(pylonImage.get_filename(), ": All pylons were detected.")
            else:
                print(pylonImage.get_filename(), "contains", pylonImage.get_actual_count(), "pylons,", pylonImage.get_supposed_count(), "were detected.")

        else:
            print(pylonImage.get_filename(), ":", pylonImage.get_supposed_count(), "pylons were detected.")

    if actualTxtFilePath is not None:
        print("Overall result:", foundPylons, "of", existingPylons, "detected.")
    else:
        print("Overall result:", foundPylons, "pylons detected.")


