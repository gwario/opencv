#!/usr/bin/env python

'''
This sample demonstrates Canny edge detection.

Usage: 
  squares.py <files> [...]

  Trackbars control edge thresholds.

'''

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy

# built-in module
import sys
import os

if __name__ == '__main__':
    print(__doc__)

    for fn in sys.argv[1:]:

        img = cv2.imread(fn)

        resBlue = create_blue_img(img)
        resYellow = create_yellow_img(img)
        resRed = create_red_img(img)
        resGreen = create_green_img(img)
        resWhite = create_white_img(img)

        resComb = resYellow + resBlue + resRed + resWhite# + resGreen

        filename, file_extension = os.path.splitext(fn)

        cv2.imwrite(filename+"_red"+file_extension, resRed)
        cv2.imwrite(filename+"_yellow"+file_extension, resYellow)
        cv2.imwrite(filename+"_white"+file_extension, resWhite)
        cv2.imwrite(filename+"_blue"+file_extension, resBlue)
        #cv2.imwrite(filename+"_green"+file_extension, resGreen)
        cv2.imwrite(filename+"_all"+file_extension, resComb)
