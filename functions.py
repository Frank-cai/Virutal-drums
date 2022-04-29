import cv2 as cv
import numpy as np

# source: https://stackoverflow.com/a/44659589
def image_resize(image, width=None, height=None, inter=cv.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]
    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image
    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)
    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv.resize(image, dim, interpolation=inter)
    # return the resized image
    return resized


# recognize hit gesture with index finger and middle finger straight
def gesture(hand, joint_list):

    angle = np.zeros(4)
    n = 0
    for joint in joint_list:
        point_A = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
        point_O = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
        point_B = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])
        A = point_A - point_O
        B = point_B - point_O
        angle[n] = np.arccos(A.dot(B)/(np.linalg.norm(A)*np.linalg.norm(B)))
        n = n+1

    if angle[0] > 2.5 and angle[1] > 2.5:  # and angle[2]<2.0 and angle[3]<2.0:
        return True
    else:
        return False
