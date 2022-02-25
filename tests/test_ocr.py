from unittest import TestCase
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../src"))
import src.ocr as ocr
import cv2


class TestOcr(TestCase):
    # Global variables
    OCR = ocr.Ocr()

    def test_ocr_prediction_car(self):
        """
        Given picture
        When OCR pytesseract is inferred
        Then true for equals result
        """

        # Open picture into test resources
        path_to_license_plate = "res/AA-434-AB.jpg"
        picture = cv2.imread(path_to_license_plate)

        # Inference with OCR pytesseract
        actual = "".join(self.OCR.ocr_prediction(picture).split()).replace("\n", "")
        expected = "AA-434-AB"

        # Test if OCR found the car plate
        self.assertEqual(expected, actual, msg="Test if OCR found the car plate.")

    def test_ocr_prediction_truck(self):
        """
        Given picture
        When OCR pytesseract is inferred
        Then true for equals result
        """
        # Open picture into test resources
        path_to_license_plate = "res/FE-010-HL.jpg"
        picture = cv2.imread(path_to_license_plate)

        # Inference with OCR pytesseract
        actual = "".join(self.OCR.ocr_prediction(picture).split()).replace("\n", "")
        expected = "FE-010-HL"

        # Test if OCR found the truck plate.
        self.assertEqual(expected, actual, msg="Test if OCR found the truck plate.")
