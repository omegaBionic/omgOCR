import logging
from math import sqrt

import cv2
import imutils
import numpy as np

import displayplate


class PreTreatment:
    def __init__(self, ARG_DEBUG):
        """
        :param ARG_DEBUG: Enable debug
        """
        # Get logger
        self.logger = logging.getLogger("Core.PreTreatment")
        self.logger.debug("Constructor called, PreTreatment instantiated.")

        # Define vars
        self.ARG_DEBUG = ARG_DEBUG
        self.DISPLAY = displayplate.DisplayPlate(self.ARG_DEBUG)
        self.debug_color_0 = (255, 0, 0)
        self.debug_color_1 = (0, 165, 255)

    def cos_a(self, distance_bc, distance_ac):
        """
        cos of alpha = BC / AC
        :param distance_bc: distance between b and c
        :param distance_ac: distance between a and c
        :return: angle cos of alpha
        """

        return distance_bc / distance_ac * 100

    def sqr(self, a):
        return a * a

    def distance(self, point_0, point_1):
        x_1 = point_0[0]
        y_1 = point_0[1]
        x_2 = point_1[0]
        y_2 = point_1[1]
        return sqrt(self.sqr(y_2 - y_1) + self.sqr(x_2 - x_1))

    def get_best_rotation(self, screen_cnt, cropped, debug_picture):
        """
        This function is used for get best rotation
        :param screen_cnt: contours points
        :param cropped: cropped frame
        :param debug_picture: debug_picture frame
        :returns: cropped, debug_picture, rotation
        """
        self.logger.info("Calculate best rotation is in running.")

        # Debug
        self.logger.debug("Calculate average between 2 upper points for get the middle.")
        self.logger.debug("screen_cnt: '{}'".format(screen_cnt))
        self.logger.debug("screen_cnt[0]: '{}'".format(screen_cnt[0][0]))  # Left up
        self.logger.debug("screen_cnt[1]: '{}'".format(screen_cnt[1][0]))  # Right up
        self.logger.debug("screen_cnt[2]: '{}'".format(screen_cnt[2][0]))  # Left bottom
        self.logger.debug("screen_cnt[3]: '{}'".format(screen_cnt[2][0]))  # Right bottom

        # Calculate average between 2 upper points for get the middle
        self.logger.debug("Calculate average between 2 upper points for get the middle.")
        average_x = int((screen_cnt[0][0][0] + screen_cnt[1][0][0]) / 2)
        average_y = int((screen_cnt[0][0][1] + screen_cnt[1][0][1]) / 2)
        average_point = (average_x, average_y)
        self.logger.debug(("average_point: '{}'".format(average_point)))
        # Draw average_point
        cv2.circle(debug_picture, average_point, radius=3, color=self.debug_color_0, thickness=-1)

        # Get cos a = (BC)/(AC)
        self.logger.debug("Get cos a = (bc)/(ac).")

        # Get a, b and c and display
        a = (debug_picture.shape[1], average_point[1])
        b = tuple(screen_cnt[1][0])
        c = tuple(screen_cnt[0][0])
        self.logger.debug("a: '{}'".format(a))
        self.logger.debug("b: '{}'".format(b))
        self.logger.debug("c: '{}'".format(c))
        cv2.circle(debug_picture, a, radius=3, color=self.debug_color_0, thickness=-1)
        cv2.circle(debug_picture, b, radius=3, color=self.debug_color_0, thickness=-1)
        cv2.circle(debug_picture, c, radius=3, color=self.debug_color_0, thickness=-1)

        # Draw triangle for debug
        overlay = debug_picture.copy()
        triangle_cnt = np.array([a, b, c])
        cv2.drawContours(overlay, [triangle_cnt], 0, (0, 255, 0), -1)
        debug_picture = cv2.addWeighted(overlay, 0.4, debug_picture, 1 - 0.4, 0)

        # cos a = (BC)/(AC)
        distance_bc = self.distance(b, c)
        distance_ac = self.distance(a, c)
        cos_a = self.cos_a(distance_bc, distance_ac)
        self.logger.debug("distance_bc: '{}'".format(distance_bc))
        self.logger.debug("distance_ac: '{}'".format(distance_ac))
        self.logger.debug("cos_a: '{}'".format(cos_a))
        self.DISPLAY.debug_display_picture("ROTATE_before", cropped, 0)

        # Correct the rotation
        if b > c:
            cropped = imutils.rotate_bound(cropped, -cos_a)
        else:
            cropped = imutils.rotate_bound(cropped, cos_a)
        self.DISPLAY.debug_display_picture("ROTATE_after", cropped, 0)

        # Return picture dans rotation applied
        return cropped, debug_picture
