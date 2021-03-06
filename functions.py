import cv2 as cv
import numpy as np


# recognize hit gesture with index finger and middle finger straight
def gesture(hand, joint_list, index, results):
    angle = np.zeros(4)
    n = 0
    for joint in joint_list:
        point_A = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y])
        point_O = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y])
        point_B = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])
        A = point_A - point_O
        B = point_B - point_O
        angle[n] = np.arccos(A.dot(B) / (np.linalg.norm(A) * np.linalg.norm(B)))
        n = n + 1

    lr = results.multi_handedness[index].classification[0].index
    if angle[0] > 2.5 and angle[1] > 2.5:  # and angle[2]<2.0 and angle[3]<2.0:
        return True, lr
    else:
        return False, lr


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


# configure drum images
def image_config(image_path, frame_w, frame_h, border_offset, image_desired_position):
    picture_height = frame_h * 0.25

    image = cv.imread(image_path, cv.IMREAD_UNCHANGED)
    image = image_resize(image, height=int(picture_height))
    image_h, image_w, image_c = image.shape

    if image_desired_position == 1:
        image_tl_x = border_offset
        image_tl_y = border_offset
    elif image_desired_position == 2:
        image_tl_x = frame_w - image_w - border_offset
        image_tl_y = border_offset
    elif image_desired_position == 3:
        image_tl_x = border_offset
        image_tl_y = frame_h - image_h - border_offset
    elif image_desired_position == 4:
        image_tl_x = int((frame_w - image_w) / 2)
        image_tl_y = frame_h - image_h - border_offset
    elif image_desired_position == 5:
        image_tl_x = frame_w - image_w - border_offset
        image_tl_y = frame_h - image_h - border_offset

    image_br_x = image_tl_x + image_w
    image_br_y = image_tl_y + image_h

    return image, image_tl_x, image_tl_y, image_br_x, image_br_y


def get_label(index, hand, results, width, height):
    output = None
    for idx, classification in enumerate(results.multi_handedness):
        if idx == index:
            # Process results
            label = classification.classification[0].label
            text = '{}'.format(label)

            # Extract Coordinates
            coords = tuple(np.multiply(np.array((hand.landmark[0].x, hand.landmark[0].y)), [width, height]).astype(int))
            output = text, coords

    return output
