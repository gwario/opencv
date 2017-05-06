import numpy
import cv2

lower_blue = numpy.array([90, 0, 0])
upper_blue = numpy.array([255, 130, 130])

lower_yellow = numpy.array([0, 130, 130])
upper_yellow = numpy.array([120, 255, 255])

lower_red = numpy.array([0, 0, 120])
upper_red = numpy.array([150, 150, 255])

lower_green = numpy.array([0, 130, 0])
upper_green = numpy.array([130, 255, 130])

lower_white = numpy.array([140, 140, 140])
upper_white = numpy.array([255, 255, 255])

def is_blueish(color):

    for idx in range(len(color)):
        if color[idx] < lower_blue[idx] or color[idx] > upper_blue[idx]:
            return False

    return True


def is_redish(color):

    for idx in range(len(color)):
        if color[idx] < lower_red[idx] or color[idx] > upper_red[idx]:
            return False

    return True


def is_yellowish(color):

    for idx in range(len(color)):
        if color[idx] < lower_yellow[idx] or color[idx] > upper_yellow[idx]:
            return False

    return True


def is_greenish(color):

    for idx in range(len(color)):
        if color[idx] < lower_green[idx] or color[idx] > upper_green[idx]:
            return False

    return True


def is_whiteish(color):

    for idx in range(len(color)):
        if color[idx] < lower_white[idx] or color[idx] > upper_white[idx]:
            return False

    return True


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


MAX_COLOR = False


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


def create_blue_img(image):
    #make all nonzero pure blue
    return create_color_range_img(image, lower_blue, upper_blue)


def create_yellow_img(image):

    return create_color_range_img(image, lower_yellow, upper_yellow)


def create_red_img(image):

    return create_color_range_img(image, lower_red, upper_red)


def create_white_img(image):

    return create_color_range_img(image, lower_white, upper_white)

