import glob
import logging
import os

import cv2

import ocrutils
from plate import Plate


class Mock:
    def __init__(self, frame_path):
        # Get logger
        self.logger = logging.getLogger("Core.Mock")

        # Define vars
        self.path_for_license_plates = os.getcwd() + frame_path + "/*"
        self.logger.info("self.path_for_license_plates: '{}'".format(self.path_for_license_plates))

    def get_frames(self):
        frames = []
        list_license_plates = []
        for path_to_license_plate in glob.glob(self.path_for_license_plates, recursive=False):
            # Get plate into file name
            if ocrutils.OcrUtils.is_windows():
                license_plate_file = path_to_license_plate.split("\\")[-1]
            else:
                license_plate_file = path_to_license_plate.split("/")[-1]
            license_plate, _ = os.path.splitext(license_plate_file)
            list_license_plates.append(Plate(license_plate))

            frames.append(cv2.imread(path_to_license_plate, cv2.IMREAD_COLOR))

        return list_license_plates, frames
