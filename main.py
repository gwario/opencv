#!/usr/bin/env python
# coding: utf8

import numpy as np
import cv2

img = cv2.imread('14729.png')

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()