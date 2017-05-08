#!/usr/bin/env python

'''
Finds pylons in files

Usage:
  match_color.py <files> [...]

'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy
import statemachine
import color_utilities


# built-in module
import sys
import os
import shutil


# window size in pixel

#dx = 10# 39 of 29
#dy = 13

#dx = 7# 35 of 29
#dy = 16

#dx = 8# 34 of 29
#dy = 18

dx = 10# 31 of 29
dy = 14

maxColorGap = dy # TODO only one "unexpected" color window is allowed between the pylon color areas
maxMatchGap = (3*dx, dy) # a 2 column distance is accepted within a real match (recognized as one pylon)

# mean or average to get the color
AVG_NOT_MEAN = False

# also modify color component value ranges in color_utilities.py


def combine_area(colIdx, rowIdx, windowMatrix, combineWindow):
    """x,y, the area and the output image"""

    if AVG_NOT_MEAN:
        avg_color_per_row = numpy.average(windowMatrix, axis=0)
        avg_color = numpy.average(avg_color_per_row, axis=0)
    else:
        avg_color_per_row = numpy.mean(windowMatrix, axis=0)
        avg_color = numpy.mean(avg_color_per_row, axis=0)

    if color_utilities.is_redish(avg_color):
        cv2.rectangle(combineWindow, (colIdx, rowIdx), (colIdx + dx, rowIdx + dy), (0, 0, 255), -1)
    elif color_utilities.is_yellowish(avg_color):
        cv2.rectangle(combineWindow, (colIdx, rowIdx), (colIdx + dx, rowIdx + dy), (0, 255, 255), -1)
    elif color_utilities.is_blueish(avg_color):
        cv2.rectangle(combineWindow, (colIdx, rowIdx), (colIdx + dx, rowIdx + dy), (255, 0, 0), -1)
    elif color_utilities.is_whiteish(avg_color):
        cv2.rectangle(combineWindow, (colIdx, rowIdx), (colIdx + dx, rowIdx + dy), (255, 255, 255), -1)


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

    colStep = dx
    rowStep = dy
    maxCols = len(pylon_image.get_image()[0])
    maxRows = len(pylon_image.get_image())

    combineWindow = numpy.zeros((maxRows, maxCols, 3), numpy.uint8)

    file_matches = []
    # combine pixels
    for colIdx in range(0, maxCols, colStep):

        column_searcher = statemachine.MatchSearcher("filename")
        column_searcher.dx = dx
        column_searcher.dy = dy

        for rowIdx in range(0, maxRows, rowStep):
            column_searcher.currentPos = (colIdx, rowIdx)

            #doesn't really help, but makes it even slower
            #windowMatrix = pylon_image.get_image()[rowIdx:rowIdx + dy, colIdx:colIdx + dx]
            #combine_area(colIdx, rowIdx, windowMatrix, combineWindow)

            #windowMatrix = combineWindow[rowIdx:rowIdx + dy, colIdx:colIdx + dx]
            windowMatrix = pylon_image.get_image()[rowIdx:rowIdx + dy, colIdx:colIdx + dx]

            interpret_area(windowMatrix, column_searcher)

        # column end
        column_searcher.currentPos = (colIdx, maxRows)  # if the match goes to the end of the column we set to the last pixel
        column_searcher.foundColumnEnd()

        file_matches.extend(column_searcher.matches)

    # file end
    # the original
    #cv2.imshow("combineWindow", combineWindow)

    # ignore neighbor matches which belong to the same pylon i.e. sort of clustering
    # NOTE: works only for one match per column.... so two pylons which are above each other are also combined
    real_file_matches = []
    previousMatch = []
    match_combination_count = 0

    for match in list(file_matches):
        # match = [(,),(,)]
        if len(previousMatch) == 0:
            previousMatch = match
            match_combination_count = 1
        else:
            previousMatchStart = previousMatch[0]
            previousMatchEnd = previousMatch[1]

            currentMatchStart = match[0]
            currentMatchEnd = match[1]

            match_end_offset = match_combination_count * (colStep + dx)

            #print("dist:", get_x_distance(previousMatchStart, currentMatchStart), ", maxgap:", maxMatchGap[0], "+", match_end_offset)
            if get_x_distance(previousMatchStart, currentMatchStart) <= maxMatchGap[0] + match_end_offset:
                # extend previous match start y
                if currentMatchStart[1] < previousMatchStart[1]:
                    previousMatch[0] = (previousMatchStart[0], currentMatchStart[1])
                # extend previous match end x and y just in case
                if currentMatchEnd[1] > previousMatchEnd[1]:
                    previousMatch[1] = (currentMatchEnd[0], currentMatchEnd[1])
                else:
                    previousMatch[1] = (currentMatchEnd[0], previousMatchEnd[1])

                match_combination_count += 1
            else:
                # add real match
                real_file_matches.append(previousMatch)
                # reset procedure
                previousMatch = match
                match_combination_count = 1

    # add last started match search
    if len(previousMatch) != 0:
        real_file_matches.append(previousMatch)

    # write image with rectangles to file
    # mark all matches with border
    #for match in file_matches:
    #    cv2.rectangle(combineWindow, match[0], match[1], (0, 0, 255), 1)
    for match in real_file_matches:
        cv2.rectangle(pylon_image.get_image(), match[0], match[1], (0,255,255), 2)

    file_name = "result/"+pylon_image.get_filename().split('/')[-1]
    cv2.imwrite(file_name, pylon_image.get_image())


    #print(file_matches)
    #print(real_file_matches)

    # TODO there is a bug in the code for grouping matches, probably because the previous match marks always the first match of the real match

    #cv2.imshow("matches", combineWindow)
    #cv2.waitKey()

    return real_file_matches


if __name__ == '__main__':
    print(__doc__)

    for fn in sys.argv[1:]:

        filename, file_extension = os.path.splitext(fn)

        img = cv2.imread(fn)

        matches = match_color(img)

    #cv2.destroyAllWindows()
