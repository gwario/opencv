import sys
import os
import cv2
import numpy
import color_utilities

def nothing(x):
    pass

if __name__ == '__main__':
    print(__doc__)

    cv2.namedWindow('images')

    if True:

        # create trackbars for color change
        cv2.createTrackbar('Hmin', 'images', 0, 180, nothing)
        cv2.createTrackbar('Hmax', 'images', 0, 180, nothing)
        cv2.createTrackbar('Smin', 'images', 0, 255, nothing)
        cv2.createTrackbar('Smax', 'images', 0, 255, nothing)
        cv2.createTrackbar('Vmin', 'images', 0, 255, nothing)
        cv2.createTrackbar('Vmax', 'images', 0, 255, nothing)

        for path, sub_dirs, files in os.walk(sys.argv[1]):
            for filename in files:
                if filename.endswith(".png"):

                    img_orig = cv2.imread(os.path.join(path, filename))

                    Z = img_orig.reshape((-1,3))
                    Z = numpy.float32(Z)

                    # define criteria, number of clusters(K) and apply kmeans()
                    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
                    K = 30
                    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

                    # Now convert back into uint8, and make original image
                    center = numpy.uint8(center)
                    res = center[label.flatten()]
                    res2 = res.reshape((img_orig.shape))


                    img_hsv = cv2.cvtColor(res2, cv2.COLOR_BGR2HSV)


                    while(1):

                        k = cv2.waitKey(1) & 0xFF
                        if k == 27:
                            break

                        # get current positions of four trackbars
                        hmax = cv2.getTrackbarPos('Hmax', 'images')
                        hmin = cv2.getTrackbarPos('Hmin', 'images')
                        smax = cv2.getTrackbarPos('Smax', 'images')
                        smin = cv2.getTrackbarPos('Smin', 'images')
                        vmax = cv2.getTrackbarPos('Vmax', 'images')
                        vmin = cv2.getTrackbarPos('Vmin', 'images')

                        # define range of blue color in HSV
                        lower = numpy.array([hmin, smin, vmin])
                        upper = numpy.array([hmax, smax, vmax])


                        # Threshold the image to get only blue colors
                        mask = cv2.inRange(img_hsv, lowerb=lower, upperb=upper)

                        # Bitwise-AND mask and original image
                        img_color = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)

                        cv2.imshow('images', numpy.hstack((img_orig, img_color)))

    else:
        for path, sub_dirs, files in os.walk(sys.argv[1]):
            for filename in files:
                if filename.endswith(".png"):

                    img_orig = cv2.imread(os.path.join(path, filename))

                    img_hsv = cv2.cvtColor(img_orig, cv2.COLOR_BGR2HSV)
                    #img_hsv = cv2.cvtColor(cv2.cvtColor(img_orig, cv2.COLOR_YUV2BGR), cv2.COLOR_BGR2HSV)

                    cv2.imshow('filename', numpy.hstack((img_orig, img_hsv)))

                    while(1):

                        k = cv2.waitKey(1) & 0xFF
                        if k == 27:
                            break

                        cv2.imshow('red', color_utilities.create_red_img(img_hsv, color_utilities.MODE_HSV))
                        cv2.imshow('yellow', color_utilities.create_yellow_img(img_hsv, color_utilities.MODE_HSV))
                        cv2.imshow('blue', color_utilities.create_blue_img(img_hsv, color_utilities.MODE_HSV))
                        cv2.imshow('white', color_utilities.create_white_img(img_hsv, color_utilities.MODE_HSV))

    cv2.destroyAllWindows()
