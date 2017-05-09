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
import statemachine
import color_utilities


# built-in module
import sys
import os


# window size in pixel

# dx = 10# 39 of 29
# dy = 13

# dx = 7# 35 of 29
# dy = 16

# dx = 8# 34 of 29
# dy = 18

# dx = 10# 31 of 29
# dy = 14

# with de-noise
dx = 10  # 23 of 29
dy = 16

max_color_gap = dy # TODO only one "unexpected" color window is allowed between the pylon color areas
max_match_gap = (3*dx, dy) # a 2 column distance is accepted within a real match (recognized as one pylon)

# mean or average to get the color
AVG_NOT_MEAN = False

USE_DENOISE = False

# also modify color component value ranges in color_utilities.py


def combine_area(col_idx, row_idx, window_matrix, combine_window):
    """x,y, the area and the output image"""

    if AVG_NOT_MEAN:
        avg_color_per_row = numpy.average(window_matrix, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
    else:
        avg_color_per_row = numpy.mean(window_matrix, axis=0)
        avg_color = numpy.mean(avg_color_per_row, axis=0)

    if color_utilities.is_redish(avg_color):
        cv2.rectangle(combine_window, (col_idx, row_idx), (col_idx + dx, row_idx + dy), (0, 0, 255), -1)
    elif color_utilities.is_yellowish(avg_color):
        cv2.rectangle(combine_window, (col_idx, row_idx), (col_idx + dx, row_idx + dy), (0, 255, 255), -1)
    elif color_utilities.is_blueish(avg_color):
        cv2.rectangle(combine_window, (col_idx, row_idx), (col_idx + dx, row_idx + dy), (255, 0, 0), -1)
    elif color_utilities.is_whiteish(avg_color):
        cv2.rectangle(combine_window, (col_idx, row_idx), (col_idx + dx, row_idx + dy), (255, 255, 255), -1)


def interpret_area(window_matrix, column_searcher):
    """the area, the state machine"""

    if AVG_NOT_MEAN:
        avg_color_per_row = numpy.average(window_matrix, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
    else:
        avg_color_per_row = numpy.mean(window_matrix, axis=0)
        avg_color = numpy.mean(avg_color_per_row, axis=0)
    if color_utilities.is_redish(avg_color):
        column_searcher.foundRed()
    elif color_utilities.is_yellowish(avg_color):
        column_searcher.foundYellow()
    elif color_utilities.is_blueish(avg_color):
        column_searcher.foundBlue()
    elif color_utilities.is_whiteish(avg_color):
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

    # combine_window = numpy.zeros((max_rows, max_cols, 3), numpy.uint8)

    # de-noise image
    if USE_DENOISE:
        combine_window = cv2.fastNlMeansDenoisingColored(pylon_image.get_image(), None, 10, 10, 13, 17)
    else:
        combine_window = pylon_image.get_image()

    # cv2.imshow("orig", pylon_image.get_image())
    # cv2.imshow("deno", combine_window)

    # cv2.waitKey()

    file_matches = []
    # combine pixels
    for col_idx in range(0, max_cols, col_step):

        column_searcher = statemachine.MatchSearcher("filename")
        column_searcher.dx = dx
        column_searcher.dy = dy

        for row_idx in range(0, max_rows, row_step):
            column_searcher.currentPos = (col_idx, row_idx)

            # doesn't really help, but makes it even slower
            # window_matrix = pylon_image.get_image()[row_idx:row_idx + dy, col_idx:col_idx + dx]
            # combine_area(col_idx, row_idx, window_matrix, combine_window)

            window_matrix = combine_window[row_idx:row_idx + dy, col_idx:col_idx + dx]
            interpret_area(window_matrix, column_searcher)

        # column end
        column_searcher.currentPos = (col_idx, max_rows)  # if the match goes to the end of the column we set to the last pixel
        column_searcher.foundColumnEnd()

        file_matches.extend(column_searcher.matches)

    # file end
    # the original
    # cv2.imshow("combine_window", combine_window)

    # ignore neighbor matches which belong to the same pylon i.e. sort of clustering
    # NOTE: works only for one match per column.... so two pylons which are above each other are also combined
    real_file_matches = []
    previous_match = []
    match_combination_count = 0

    for match in list(file_matches):
        # match = [(,),(,)]
        if len(previous_match) == 0:
            previous_match = match
            match_combination_count = 1
        else:
            previous_match_start = previous_match[0]
            previous_matchEnd = previous_match[1]

            currentMatchStart = match[0]
            currentMatchEnd = match[1]

            match_end_offset = match_combination_count * (col_step + dx)

            # print("dist:", get_x_distance(previous_match_start, currentMatchStart), ", maxgap:", max_match_gap[0], "+", match_end_offset)
            if get_x_distance(previous_match_start, currentMatchStart) <= max_match_gap[0] + match_end_offset:
                # extend previous match start y
                if currentMatchStart[1] < previous_match_start[1]:
                    previous_match[0] = (previous_match_start[0], currentMatchStart[1])
                # extend previous match end x and y just in case
                if currentMatchEnd[1] > previous_matchEnd[1]:
                    previous_match[1] = (currentMatchEnd[0], currentMatchEnd[1])
                else:
                    previous_match[1] = (currentMatchEnd[0], previous_matchEnd[1])

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


    # print(file_matches)
    # print(real_file_matches)

    # TODO there is a bug in the code for grouping matches, probably because the previous match marks always the first match of the real match

    # cv2.imshow("matches", combine_window)
    # cv2.waitKey()

    return real_file_matches


if __name__ == '__main__':
    print(__doc__)

    for fn in sys.argv[1:]:

        filename, file_extension = os.path.splitext(fn)

        img = cv2.imread(fn)

        matches = match_color(img)

    # cv2.destroyAllWindows()
