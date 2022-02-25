import logging
import os
from enum import Enum


class OcrUtils:
    def __init__(self):
        # Get logger
        self.logger = logging.getLogger("Core.OcrUtils")
        self.logger.debug("Constructor called, OcrUtils instantiated.")

    @staticmethod
    def is_windows():
        """
        This method is used for get Boolean for OS type
        :return: Return True for windows and False for Linux or other :)
        """
        return os.name == "nt"

    class InputMode(Enum):
        """
        This class is used for enum usage mode.
        """
        MOCK = 1
        RASPBERRY_CAMERA = 2

        def __str__(self):
            return self.name

        def __repr__(self):
            return str(self)

        def argparse(self, s):
            try:
                return self.InputMode[s.upper()]
            except KeyError:
                return s
