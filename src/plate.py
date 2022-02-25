import logging


class Plate:
    def __init__(self, str_plate):
        """
        __init__ Plate
        :return: Plate object
        """
        # Get logger
        self.logger = logging.getLogger("Core.Plates")

        self.str_plate = str_plate

    def __repr__(self):
        """
        :return: display of str_plate
        """
        self.logger.info(self.str_plate)

    def __len__(self):
        """
        :return: len of str_plate
        """
        return len(self.str_plate)

    @property
    def str_plate(self):
        """
        getter str_plate
        :return: str_plate
        """
        return self._str_plate

    @str_plate.setter
    def str_plate(self, value):
        """
        setter str_plate
        :return: str_plate
        """
        self._str_plate = str(value)

    @str_plate.deleter
    def str_plate(self):
        """
        deleter str_plate
        :return: str_plate
        """
        del self._str_plate

    def split(self):
        """
        split str_plate
        :return: Nothing
        """
        self.str_plate = "".join(self.str_plate.split())

    def replace(self, old_value, new_value):
        """
        replace str_plate
        :return: Nothing
        """
        self.str_plate = self.str_plate.replace(old_value, new_value)
