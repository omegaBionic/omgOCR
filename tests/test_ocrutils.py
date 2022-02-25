from unittest import TestCase
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../src"))
import src.ocrutils as ocrutils
import cv2


class TestOcrUtils(TestCase):
    def test_get_os(self):
        """
        Given nothing
        When get os from ocrutils
        Then os is Windows or Linux
        """
        # Open picture into test resources
        path_to_license_plate = "res/AA-434-AB.jpg"
        picture = cv2.imread(path_to_license_plate)

        # Inference with OCR pytesseract
        actual = ocrutils.OcrUtils.get_os()
        expected = True

        # Test if is boolean, other types is fail
        self.assertIs(expected, actual, msg="Test if is boolean, other types is fail.")
