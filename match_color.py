#!/usr/bin/env python

"""
Finds pylons in files

Usage:
  match_color.py <files> [...]

"""

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy
import colorsys
import statemachine
import color_utilities
import sys
import copy
import os


# window size in pixel
dx = 8  # 23 of 29
dy = 8

max_color_gap = dy # TODO only one "unexpected" color window is allowed between the pylon color areas
max_match_gap = (3*dx, dy) # a 2 column distance is accepted within a real match (recognized as one pylon)

# mean or average to get the color
AVG_NOT_MEAN = False

USE_DENOISE = False
USE_KMEANS = True
TOP_DOWN = False

# also modify color component value ranges in color_utilities.py


def combine_area(col_idx, row_idx, window_matrix, img, cspace = color_utilities.MODE_RGB):
    """x,y, the area and the output image"""

    if AVG_NOT_MEAN:
        avg_color_per_row = numpy.average(window_matrix, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
    else:
        avg_color_per_row = numpy.median(window_matrix, axis=0)
        avg_color = numpy.median(avg_color_per_row, axis=0)


    if cspace == color_utilities.MODE_RGB:

        color_red = (255, 0, 0)
        color_yellow = (255, 255, 0)
        color_blue = (0, 0, 255)
        color_white = (255, 255, 255)
        color_red = reversed(color_red)
        color_yellow = reversed(color_yellow)
        color_blue = reversed(color_blue)
        color_white = reversed(color_white)

    elif cspace == color_utilities.MODE_HSV:

        color_red = (0, 255, 255)
        color_yellow = (30, 255, 255)
        color_blue = (120, 255, 255)
        color_white = (0, 0, 255)

    if color_utilities.is_redish(avg_color, cspace):
        cv2.rectangle(img, (col_idx, row_idx), (col_idx + dx, row_idx + dy), color_red, -1)
    elif color_utilities.is_yellowish(avg_color, cspace):
        cv2.rectangle(img, (col_idx, row_idx), (col_idx + dx, row_idx + dy), color_yellow, -1)
    elif color_utilities.is_blueish(avg_color, cspace):
        cv2.rectangle(img, (col_idx, row_idx), (col_idx + dx, row_idx + dy), color_blue, -1)
    elif color_utilities.is_whiteish(avg_color, cspace):
        cv2.rectangle(img, (col_idx, row_idx), (col_idx + dx, row_idx + dy), color_white, -1)


def interpret_area(window_matrix, column_searcher, cspace = color_utilities.MODE_RGB):
    """the area, the state machine"""

    if AVG_NOT_MEAN:
        avg_color_per_row = numpy.average(window_matrix, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
    else:
        avg_color_per_row = numpy.mean(window_matrix, axis=0)
        avg_color = numpy.mean(avg_color_per_row, axis=0)

    if color_utilities.is_redish(avg_color, cspace):
        column_searcher.foundRed()
    elif color_utilities.is_yellowish(avg_color, cspace):
        column_searcher.foundYellow()
    elif color_utilities.is_blueish(avg_color, cspace):
        column_searcher.foundBlue()
    elif color_utilities.is_whiteish(avg_color, cspace):
        column_searcher.foundWhite()
    else:
        column_searcher.foundOther()


def get_x_distance(point_1, point_2):
    return abs(point_1[0] - point_2[0])


def match_color(pylon_image):

    col_step = dx
    row_step = dy
    max_cols = len(pylon_image.get_image()[0])
    max_rows = len(pylon_image.get_image())

    # de-noise image
    if USE_DENOISE:
        img_clustered = cv2.fastNlMeansDenoisingColored(pylon_image.get_image(), None, 10, 10, 13, 17)
    else:
        img_clustered = pylon_image.get_image()

    if USE_KMEANS:
        img_clustered = pylon_image.get_image()
        Z = img_clustered.reshape((-1,3))

        # convert to np.float32
        Z = numpy.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 25
        ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

        # Now convert back into uint8, and make original image
        center = numpy.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((img_clustered.shape))
        cv2.imshow("kmeans", res2)
        img_clustered = res2

    img_clustered = cv2.cvtColor(img_clustered, cv2.COLOR_BGR2HSV)

    file_matches = []
    for col_idx in range(0, max_cols, col_step):

        column_searcher = statemachine.MatchSearcher("filename", topdown=TOP_DOWN)
        column_searcher.dx = dx
        column_searcher.dy = dy

        for row_idx in range(0, max_rows, row_step) if TOP_DOWN else range(max_rows, 0, -row_step):
            column_searcher.currentPos = (col_idx, row_idx)

            # doesn't really help, but makes it even slower
            #window_matrix = img_clustered[row_idx:row_idx + dy, col_idx:col_idx + dx]
            #combine_area(col_idx, row_idx, window_matrix, img_clustered, color_utilities.MODE_HSV)

            window_matrix = img_clustered[row_idx:row_idx + dy, col_idx:col_idx + dx]
            interpret_area(window_matrix, column_searcher, color_utilities.MODE_HSV)

        # column end
        column_searcher.currentPos = (col_idx, max_rows)  # if the match goes to the end of the column we set to the last pixel
        column_searcher.foundColumnEnd()

        file_matches.extend(column_searcher.matches)

    # file end

    # ignore neighbor matches which belong to the same pylon i.e. sort of clustering
    # NOTE: works only for one match per column.... so two pylons which are above each other are also combined
    real_file_matches = group_matches(col_step, file_matches)


    cv2.imshow("clustered", cv2.cvtColor(img_clustered, cv2.COLOR_HSV2BGR))
    #print(file_matches)
    for match in file_matches:
        cv2.rectangle(pylon_image.get_image(), match[0], match[1], (0, 0, 0), 1)
    for match in real_file_matches:
        cv2.rectangle(pylon_image.get_image(), match[0], match[1], (0, 255, 255), 1)
    cv2.imshow("matches", pylon_image.get_image())
    cv2.waitKey()

    # print(file_matches)
    # print(real_file_matches)

    # TODO there is a bug in the code for grouping matches, probably because the previous match marks always the first match of the real match

    return real_file_matches


def group_matches(col_step, file_matches):

    real_file_matches = []
    previous_match = []
    match_combination_count = 0
    for match in list(file_matches):
        # match = [(,),(,)]
        if len(previous_match) == 0:
            previous_match = copy.deepcopy(match)
            match_combination_count = 1
        else:
            previous_match_start = previous_match[0]
            previous_matchEnd = previous_match[1]

            currentMatchStart = match[0]
            currentMatchEnd = match[1]

            match_end_offset = match_combination_count * (col_step + dx)

            # print("dist:", get_x_distance(previous_match_start, currentMatchStart), ", maxgap:", max_match_gap[0], "+", match_end_offset)
            if get_x_distance(previous_match_start, currentMatchStart) <= max_match_gap[0] + match_end_offset:
                # extend previous match start and end
                if TOP_DOWN:
                    previous_match[0] = (previous_match_start[0], min(currentMatchStart[1], previous_match_start[1]))
                    previous_match[1] = (currentMatchEnd[0], max(currentMatchEnd[1], previous_matchEnd[1]))
                else:
                    previous_match[0] = (previous_match_start[0], max(currentMatchStart[1], previous_match_start[1]))
                    previous_match[1] = (currentMatchEnd[0], min(currentMatchEnd[1], previous_matchEnd[1]))

                match_combination_count += 1
            else:
                # add real match
                real_file_matches.append(previous_match)
                # reset procedure
                previous_match = match
                match_combination_count = 1

    # add last started match search
    if len(previous_match) != 0:
        real_file_matches.append(previous_match)

    return real_file_matches


if __name__ == '__main__':
    print(__doc__)

    for fn in sys.argv[1:]:

        filename, file_extension = os.path.splitext(fn)

        img = cv2.imread(fn)

        matches = match_color(img)

    # cv2.destroyAllWindows()
