import cv2

class PylonImage:
    """
    This class represents a pylon image.
    It contains information on the number and position of pylons
    """

    __filename__ = ""
    __image__ = None
    __matches__ = None
    __actual_count__ = None
    __supposed_count__ = None

    def __init__(self, filename, actual_count=None):

        if filename != "":
            self.__filename__ = filename

        if actual_count is not None:
            if actual_count >= 0:
                self.__actual_count__ = actual_count
            else:
                raise ValueError("Actual pylon count must be greater or equal to zero.")

        image = cv2.imread(self.__filename__)
        if image is not None:
            self.__image__ = image
        else:
            raise ValueError("Invalid file.")

    def get_filename(self):
        return self.__filename__

    def get_image(self):
        return self.__image__

    def set_matches(self, matches):
        self.__matches__ = matches

    def get_matches(self):
        return self.__matches__

    def set_supposed_count(self, count):
        if count >= 0:
            self.__supposed_count__ = count
        else:
            raise ValueError("Pylon count must be greater or equal to zero.")

    def get_supposed_count(self):
        return self.__supposed_count__

    def set_actual_count(self, count):
        if count >= 0:
            self.__actual_count__ = count
        else:
            raise ValueError("Pylon count must be greater or equal to zero.")

    def get_actual_count(self):
        return self.__actual_count__

    def correctly_recognized(self):
        return self.__supposed_count__ is not None and self.__actual_count__  is not None and self.__supposed_count__ == self.__actual_count__