#!/usr/bin/env python

'''
This program detects pylons within images.

Authors: Mario Gastegger, Fritz Meiners



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
    __matches__ = None
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

    def set_matches(self, matches):
        self.__matches__ = matches

    def get_matches(self):
        return self.__matches__

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
    '''
    Compares image to list of template images and returns the top left coordinates of the matches
    and an empty list if no template matched
    '''
    matches = []

    for template in os.listdir("templates"):
        img_rgb = image.get_image()

        if (template.endswith(".png")):
            # load images and convert to grayscale
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(cv2.imread(os.path.join("templates", template)), cv2.COLOR_BGR2GRAY)

            # scale template from 0.3 to 1.5 in alternating order and perform matching
            scale_factors = [1.0, 0.9, 1.1, 0.8, 1.2, 0.7, 1.3, 0.6, 1.4, 0.5, 0.4, 0.3]
            scaled_templates = [cv2.resize(template_gray, (0,0), fx=x, fy=x) for x in scale_factors]

            for current_template in scaled_templates:
                # store variables for rectangles drawn later
                w, h = current_template.shape[::-1]

                # actual template matching
                result = cv2.matchTemplate(img_gray, current_template, cv2.TM_CCOEFF_NORMED)

                # remove all matches with too low of a matching score
                threshold = 0.7
                loc = np.where(result >= threshold)
                top_matches = zip(*loc[::-1])

                # draw rectangle at position of first match
                if len(top_matches) > 0:
                    for pt in top_matches:
                        matches += [pt]
                        cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
                        break #break after first point

                break #break after first success

        else:
            print("Skipping file " + template)

    # if matching was successful write image with rectangles to file
    if (len(matches) > 0):
        dir = "detected"
        if not os.path.exists(dir):
            os.makedirs(dir)

        file_name = "detected/matched_" + image.get_filename().split('/')[-1]
        cv2.imwrite(file_name, img_rgb)
        print("Match found for " + image.__filename__)

    return matches


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
        pylonImage.set_matches(match_templates(pylonImage))
        pylonImage.set_supposed_count(len(pylonImage.get_matches()))
        # write result to stdout TODO implement the required format
        #print(pylonImage.get_filename() + ':', pylonImage.get_supposed_count())

    print('Generating result...')

    # write results to text file
    result_file = open("results.txt", "w")
    for pylon_image in pylon_images:
        if len(pylon_image.get_matches()) > 0:
            entry = pylon_image.get_filename() + "; "

            for pt in pylon_image.get_matches():
                entry += str(pt) + ", "

            result_file.write(entry + "\n");

    result_file.close();

    # show success rate and print detection errors
    existingPylons = 0
    foundPylons = 0

    for pylonImage in pylon_images:
        foundPylons += pylonImage.get_supposed_count()

        if actualTxtFilePath is not None:
            existingPylons += pylonImage.get_actual_count()

            if not pylonImage.correctly_recognized():
                print(pylonImage.get_filename(), "contains", pylonImage.get_actual_count(), "pylons,", pylonImage.get_supposed_count(), "were detected.")

        else:
            print(pylonImage.get_filename(), ":", pylonImage.get_supposed_count(), "pylons were detected.")

    if actualTxtFilePath is not None:
        print("Overall result:", foundPylons, "of", existingPylons, "detected.")
    else:
        print("Overall result:", foundPylons, "pylons detected.")
