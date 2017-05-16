import numpy
import cv2

lower_blue_bgr = numpy.array([90, 0, 0])
upper_blue_bgr = numpy.array([255, 130, 130])
lower_yellow_bgr = numpy.array([0, 130, 130])
upper_yellow_bgr = numpy.array([120, 255, 255])
lower_red_bgr = numpy.array([0, 0, 120])
upper_red_bgr = numpy.array([140, 140, 255])
lower_green_bgr = numpy.array([0, 130, 0])
upper_green_bgr = numpy.array([130, 255, 130])
lower_white_bgr = numpy.array([150, 150, 150])
upper_white_bgr = numpy.array([255, 255, 255])

# wo kmeans
lower_blue_hsv = numpy.array([100, 145, 70])
upper_blue_hsv = numpy.array([110, 211, 205])
lower_yellow_hsv = numpy.array([15, 170, 110])
upper_yellow_hsv = numpy.array([27, 200, 255])
lower_red_hsv = numpy.array([20, 125, 230])
upper_red_hsv = numpy.array([168, 185, 249])
lower_green_hsv = numpy.array([35, 80, 60])
upper_green_hsv = numpy.array([90, 190, 200])
lower_white_hsv = numpy.array([15, 0, 120])
upper_white_hsv = numpy.array([180, 100, 255])

# w kmeans
#lower_blue_hsv = numpy.array([100, 10, 10])
#upper_blue_hsv = numpy.array([135, 245, 245])
#lower_yellow_hsv = numpy.array([19, 10, 10])
#upper_yellow_hsv = numpy.array([35, 250, 250])
#lower_white_hsv = numpy.array([0, 0, 204])
#upper_white_hsv = numpy.array([180, 50, 255])
#lower_red_hsv = numpy.array([15, 30, 100])
#upper_red_hsv = numpy.array([168, 255, 255])
#lower_green_hsv = numpy.array([35, 10, 10])
#upper_green_hsv = numpy.array([90, 245, 245])


MODE_RGB = 0
MODE_HSV = 1

#works only for rgb
MAX_COLOR = False


def is_blueish(color, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        for idx in range(len(color)):
            if color[idx] <= lower_blue_bgr[idx] or color[idx] >= upper_blue_bgr[idx]:
                return False
        return True

    elif cspace == MODE_HSV:
        return  lower_blue_hsv[0] <= color[0] and color[0] <= upper_blue_hsv[0] \
            and lower_blue_hsv[1] <= color[1] and color[1] <= upper_blue_hsv[1] \
            and lower_blue_hsv[2] <= color[2] and color[2] <= upper_blue_hsv[2]


def is_redish(color, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        for idx in range(len(color)):
            if color[idx] <= lower_red_bgr[idx] or color[idx] >= upper_red_bgr[idx]:
                return False

        return True

    elif cspace == MODE_HSV:
        return (color[0] <= lower_red_hsv[0] or color[0] >= upper_red_hsv[0]) \
            and lower_red_hsv[1] <= color[1] and color[1] <= upper_red_hsv[1] \
            and lower_red_hsv[2] <= color[2] and color[2] <= upper_red_hsv[2]


def is_yellowish(color, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        for idx in range(len(color)):
            if color[idx] <= lower_yellow_bgr[idx] or color[idx] >= upper_yellow_bgr[idx]:
                return False
        return True

    elif cspace == MODE_HSV:
        return  lower_yellow_hsv[0] <= color[0] and color[0] <= upper_yellow_hsv[0] \
            and lower_yellow_hsv[1] <= color[1] and color[1] <= upper_yellow_hsv[1] \
            and lower_yellow_hsv[2] <= color[2] and color[2] <= upper_yellow_hsv[2]


def is_greenish(color, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        for idx in range(len(color)):
            if color[idx] <= lower_green_bgr[idx] or color[idx] >= upper_green_bgr[idx]:
                return False
        return True

    elif cspace == MODE_HSV:
        return  lower_green_hsv[0] <= color[0] and color[0] <= upper_green_hsv[0] \
            and lower_green_hsv[1] <= color[1] and color[1] <= upper_green_hsv[1] \
            and lower_green_hsv[2] <= color[2] and color[2] <= upper_green_hsv[2]


def is_whiteish(color, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        for idx in range(len(color)):
            if color[idx] <= lower_white_bgr[idx] or color[idx] >= upper_white_bgr[idx]:
                return False
        return True

    elif cspace == MODE_HSV:
        return  lower_white_hsv[0] <= color[0] and color[0] <= upper_white_hsv[0] \
            and lower_white_hsv[1] <= color[1] and color[1] <= upper_white_hsv[1] \
            and lower_white_hsv[2] <= color[2] and color[2] <= upper_white_hsv[2]


def is_blue(color):

    if color[0] == 255 and color[1] == 0 and color[2] == 0:
        return True
    else:
        return False


def is_red(color):

    if color[0] == 0 and color[1] == 0 and color[2] == 255:
        return True
    else:
        return False


def is_yellow(color):

    if color[0] == 0 and color[1] == 255 and color[2] == 255:
        return True
    else:
        return False


def is_green(color):

    if color[0] == 0 and color[1] == 255 and color[2] == 0:
        return True
    else:
        return False


def is_white(color):

    if color[0] == 255 and color[1] == 255 and color[2] == 255:
        return True
    else:
        return False

def create_color_range_img(image, lowerb, upperb):

    # Threshold the image to get only blue colors
    mask = cv2.inRange(image, lowerb=lowerb, upperb=upperb)

    newimg = image.copy()

    if MAX_COLOR:
        max_color = [0, 0, 0]
        for index, value in enumerate(upperb):
            if value == 255:
                max_color[index] = 255

        for x in range(0, len(image[0])):
            for y in range(0, len(image)):
                if mask[y][x] == 255:
                    newimg[y][x] = max_color
                else:
                    newimg[y][x] = [0, 0, 0]

        return newimg
    else:
        # Bitwise-AND mask and original image
        return cv2.bitwise_and(image, image, mask=mask)


def create_blue_img(image, cspace = MODE_RGB):
    #make all nonzero pure blue
    if cspace == MODE_RGB:
        return create_color_range_img(image, lower_blue_bgr, upper_blue_bgr)
    elif cspace == MODE_HSV:
        return create_color_range_img(image, lower_blue_hsv, upper_blue_hsv)


def create_yellow_img(image, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        return create_color_range_img(image, lower_yellow_bgr, upper_yellow_bgr)
    elif cspace == MODE_HSV:
        return create_color_range_img(image, lower_yellow_hsv, upper_yellow_hsv)


def create_red_img(image, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        return create_color_range_img(image, lower_red_bgr, upper_red_bgr)
    elif cspace == MODE_HSV:
        return create_color_range_img(image, lower_red_hsv, upper_red_hsv)


def create_white_img(image, cspace = MODE_RGB):

    if cspace == MODE_RGB:
        return create_color_range_img(image, lower_white_bgr, upper_white_bgr)
    elif cspace == MODE_HSV:
        return create_color_range_img(image, lower_white_hsv, upper_white_hsv)
