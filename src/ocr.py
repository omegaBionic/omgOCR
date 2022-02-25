import logging

import cv2
import pytesseract

import ocrutils


class Ocr:
    def __init__(self,
                 config='-l fra --oem 3 --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- '):
        """
        :param config: configuration for ocr
        :arg:
        --oem
        0 Legacy engine only.
        1 Neural nets LSTM engine only.
        2 Legacy + LSTM engines. <-- BEST
        3 Default, based on what is available.

        --psm
        0    Orientation and script detection (OSD) only.
        1    Automatic page segmentation with OSD.
        2    Automatic page segmentation, but no OSD, or OCR.
        3    Fully automatic page segmentation, but no OSD. (Default)
        4    Assume a single column of text of variable sizes.
        5    Assume a single uniform block of vertically aligned text.
        6    Assume a single uniform block of text.
        7    Treat the image as a single text line.
        8    Treat the image as a single word.
        9    Treat the image as a single word in a circle.
        10    Treat the image as a single character.
        11    Sparse text. Find as much text as possible in no particular order. <-- Best
        12    Sparse text with OSD.
        13    Raw line. Treat the image as a single text line,
                                bypassing hacks that are Tesseract-specific.
        """
        # Get logger
        self.logger = logging.getLogger("Core.Ocr")
        self.logger.debug("Constructor called, Ocr instantiated.")

        # Define config
        self.config = config

        # Windows need to define pytesseract path
        if ocrutils.OcrUtils.is_windows():
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def ocr_prediction(self, picture):
        """
        This method is used for call OCR pytesseract
        :param picture: input picture
        :param config: configuration, like allowed characters
        :return: string found
        """
        return pytesseract.image_to_string(picture, config=self.config)
