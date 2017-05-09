#!/usr/bin/env python

'''
This program detects pylons within images.

Authors: Mario Gastegger, Fritz Meiners
'''

# Python 2/3 compatibility
from __future__ import print_function

import match_color
import match_templates
import pylon_image
import shutil
import time
import cv2


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

    for path, sub_dirs, files in os.walk(img_dir_path):

        for filename in files:

            if filename.endswith(".png"):
                try:
                    pylonImage = pylon_image.PylonImage(os.path.join(path, filename), 0)

                    if filename in actual_counts:
                        pylonImage.set_actual_count(actual_counts[filename])

                    pylon_images.append(pylonImage)

                except (ValueError, SyntaxError):
                    print ("Failed to create PylonImage from %s" % filename)
            else:
                print('Skipping ', filename)

    print(len(pylon_images), 'PylonImages processed.')

    return pylon_images


def write_results_file(pylon_image):

    entry = "{},{}".format(pylon_image.get_filename(), len(pylon_image.get_matches()))
    for rect in pylon_image.get_matches():
        for pt in rect:
            entry += ",{},{}".format(pt[0], pt[1])
    result_file.write(entry + "\n")


def write_results_images(pylon_image):

    for match in pylon_image.get_matches():
        cv2.rectangle(pylon_image.get_image(), match[0], match[1], (0, 0, 0), 2)

    path_parts = pylon_image.get_filename().split('/')

    file_name = path_parts[-1]
    subdir = None

    if len(path_parts) > 1:

        subdir = "results/" + path_parts[-2]

        if not os.path.exists(subdir):
            os.makedirs(subdir)

    if subdir is None:
        cv2.imwrite(file_name, pylon_image.get_image())
    else:
        cv2.imwrite(subdir + "/" + file_name, pylon_image.get_image())


if __name__ == '__main__':

    import sys, os, argparse

    parser = argparse.ArgumentParser(description='This program detects pylons within images.')
    parser.add_argument('--actual', type=argparse.FileType('r'), help='''Compares the number of detected pylons in an image with the actual number of pylons.
        The actual number of pylons is read from the file <ACTUAL>, which contains one file per line.
        The filename and the number of pylons is separated by a semicolon.''')
    parser.add_argument('imagePath', nargs=1, help='The path to the image files.')
    parser.add_argument('--method', required=True, help='''"color" for the color scanning + color transition state machine (takes three times longer but performs much better)
        "template" for the template matching.''')
    parser.add_argument('--debug', action='store_true', help='''Prints to stdout and writes the images, with matches marked, to the results directory''')
    parser.set_defaults(feature = False)

    args = parser.parse_args()

    imgDirPath = args.imagePath[0]
    actualTxtFilePath = args.actual
    method = args.method

    #print(args)

    if not os.path.exists(imgDirPath) or not os.path.isdir(imgDirPath):

        print("Path to image files does not exist!")
        sys.exit(1)

    if method is None:
        print("No method specified!")
        sys.exit(1)
    elif method != 'template' and method != 'color':
        print("Invalid method!")
        sys.exit(1)

    print('Processing PylonImages...')

    pylon_images = pylon_images_from_folder(imgDirPath, actualTxtFilePath)

    print('Analyzing...')

    for pylonImage in pylon_images:
        # analyze image
        start = time.time()
        if method == "template":
            pylonImage.set_matches(match_templates.match_templates(pylonImage))
        elif method == "color":
            pylonImage.set_matches(match_color.match_color(pylonImage))

        pylonImage.set_supposed_count(len(pylonImage.get_matches()))
        if args.debug:
            print("{}: detected {} pylons in {:.2f} sec.".format(pylonImage.get_filename(), pylonImage.get_supposed_count(), (time.time() - start) % 1000))

    print('Generating result...')

    if args.debug:
        resdir = "results"
        if not os.path.exists(resdir):
            os.makedirs(resdir)
        else:
            shutil.rmtree(resdir)
            os.makedirs(resdir)

    # write results to text file
    result_file = open("results.txt", "w")
    for pylon_image in pylon_images:

        write_results_file(pylon_image)

        if args.debug:
            write_results_images(pylon_image)

    result_file.close()

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
            if args.debug:
                print(pylonImage.get_filename(), ":", pylonImage.get_supposed_count(), "pylons were detected.")

    if actualTxtFilePath is not None:
        print("Overall result:", foundPylons, "of", existingPylons, "detected.")
    else:
        print("Overall result:", foundPylons, "pylons detected.")
