#!/usr/bin/env python

'''
Simple "Square Detector" program.

Loads several images sequentially and tries to find squares in each image.
'''

# Python 2/3 compatibility
import sys
PY3 = sys.version_info[0] == 3

if PY3:
    xrange = range

import numpy as np
import cv2

def nothing(*arg):
    pass

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img, thrs1, thrs2, ksize):
    img = cv2.GaussianBlur(img, (ksize, ksize), 0)
    cv2.imshow('squares', img)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, thrs1, thrs2, apertureSize=7)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

if __name__ == '__main__':
    from glob import glob
    cv2.namedWindow('squares')
    cv2.createTrackbar('thrs1', 'squares', 0, 50000, nothing)
    cv2.createTrackbar('thrs2', 'squares', 50, 50000, nothing)
    cv2.createTrackbar('ksize', 'squares', 5, 20, nothing)

    for fn in glob('./*_*.png'):
        img = cv2.imread(fn)

        while True:
            thrs1 = cv2.getTrackbarPos('thrs1', 'squares')
            thrs2 = cv2.getTrackbarPos('thrs2', 'squares')
            ksize = cv2.getTrackbarPos('ksize', 'squares')
            squares = find_squares(img, thrs1, thrs2, ksize)
            cv2.drawContours( img, squares, -1, (0, 255, 0), 3 )
            cv2.imshow('squares', img)
            ch = cv2.waitKey()
            print("iter")
            if ch == 27:
                break

    cv2.destroyAllWindows()
