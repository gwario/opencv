import cv2
import os
import numpy as np

def match_templates(image):
    '''
    Compares image to list of template images and returns the top left coordinates of the matches
    and an empty list if no template matched
    '''
    # [[(x1, y1), (x2, y2)]
    matches = []

    for template in os.listdir("templates"):
        img_rgb = image.get_image()

        if (template.endswith(".png")):
            # load images and convert to grayscale
            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(cv2.imread(os.path.join("templates", template)), cv2.COLOR_BGR2GRAY)

            # scale template from 0.3 to 1.5 in alternating order and perform matching
            scale_factors = [1.0, 0.9, 1.1, 0.8, 1.2, 0.7, 1.3, 0.6, 1.4, 0.5, 0.4, 0.3]
            scaled_templates = [cv2.resize(template_gray, (0,0), fx=x, fy=x) for x in scale_factors]

            for current_template in scaled_templates:
                # store variables for rectangles drawn later
                w, h = current_template.shape[::-1]

                # actual template matching
                result = cv2.matchTemplate(img_gray, current_template, cv2.TM_CCOEFF_NORMED)

                # remove all matches with too low of a matching score
                threshold = 0.7
                loc = np.where(result >= threshold)
                top_matches = zip(*loc[::-1])

                # draw rectangle at position of first match
                if len(top_matches) > 0:
                    for pt in top_matches:
                        matches.append([pt, (pt[0] + w, pt[1] + h)])
                        #cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,255,255), 2)
                        break #break after first point

                break #break after first success

        else:
            print("Skipping file " + template)

    # if matching was successful write image with rectangles to file
    #if (len(matches) > 0):
    #dir = "detected"
    #if not os.path.exists(dir):
    #    os.makedirs(dir)

    #file_name = "detected/" + image.get_filename().split('/')[-1]
    #cv2.imwrite(file_name, img_rgb)
    #print("Match found for " + image.__filename__)

    return matches