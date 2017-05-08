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

import match_color
import match_templates
import pylon_image
import shutil


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
                pylonImage = pylon_image.PylonImage(os.path.join(img_dir_path, filename), 0)

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

    #print(args)

    if not os.path.exists(imgDirPath) or not os.path.isdir(imgDirPath):

        print("Path to image files does not exist!")
        sys.exit(1)

    dir = "detected"
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)

    dir = "result"
    if not os.path.exists(dir):
        os.makedirs(dir)
    else:
        shutil.rmtree(dir)
        os.makedirs(dir)


    print('Processing PylonImages...')

    pylon_images = pylon_images_from_folder(imgDirPath, actualTxtFilePath)

    print('Analyzing...')

    for pylonImage in pylon_images:
        # analyze image
        #pylonImage.set_matches(match_templates.match_templates(pylonImage))
        pylonImage.set_matches(match_color.match_color(pylonImage))
        pylonImage.set_supposed_count(len(pylonImage.get_matches()))
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
