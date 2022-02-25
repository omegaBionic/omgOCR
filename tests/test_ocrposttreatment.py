from unittest import TestCase
import sys
import os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/../src"))
import src.ocrposttreatment as ocrposttreatment


class TestPostTreatment(TestCase):
    def test_regex_plate_spaces(self):
        """
        Given plate with spaces
        When regex processing
        Then regex give good license plate
        """
        # Input plate
        input_plate = "         WW    -    453     -    AA       "

        # Inference with OCR pytesseract
        actual = ocrposttreatment.PostTreatment.regex_plate(input_plate)
        expected = "WW-453-AA"

        # Check if regex found the great license plate
        self.assertEqual(expected, actual, msg="Check if regex found the great license plate for  added 'spaces'.")

    def test_regex_plate_digits(self):
        """
        Given plate with digits
        When regex processing
        Then regex give good license plate
        """
        # Input plate
        input_plate = "65AW24-453-12AA11565116561"

        # Inference with OCR pytesseract
        actual = ocrposttreatment.PostTreatment.regex_plate(input_plate)
        expected = "AW-453-AA"

        # Check if regex found the great license plate
        self.assertEqual(expected, actual, msg="Check if regex found the great license plate for  added 'digits'.")

    def test_regex_plate_letters_uppercase(self):
        """
        Given plate with letters in uppercase
        When regex processing
        Then regex give good license plate
        """
        # Input plate
        input_plate = "WDA-A453E-PARCLLLDADADAZDDADWDZADSQDQ"

        # Inference with OCR pytesseract
        actual = ocrposttreatment.PostTreatment.regex_plate(input_plate)
        expected = "WD-453-PA"

        # Check if regex found the great license plate
        self.assertEqual(expected, actual, msg="Check if regex found the great license plate for  added 'letters'.")

    def test_regex_plate_letters_lowercase(self):
        """
        Given plate with letters in lowercase
        When regex processing
        Then regex give good license plate
        """
        # Input plate
        input_plate = "zodiacWD-access453xcode-passedPAtaxic"

        # Inference with OCR pytesseract
        actual = ocrposttreatment.PostTreatment.regex_plate(input_plate)
        expected = "WD-453-PA"

        # Check if regex found the great license plate
        self.assertEqual(expected, actual, msg="Check if regex found the great license plate for  added 'letters'.")
