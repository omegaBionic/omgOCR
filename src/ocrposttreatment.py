import logging
import re


class PostTreatment:
    def __init__(self):
        # Get logger
        self.logger = logging.getLogger("Core.PostTreatment")
        self.logger.debug("Constructor called, PostTreatment instantiated.")

    @staticmethod
    def regex_plate(filter_predicted_result):
        """
        This function is used for regex plate processing.
        :param filter_predicted_result: plate that will be processed
        :return: processed plate with regex
        """
        # Declare regex
        r_left = re.compile('^.*?([A-Z]{2}).*?$')
        r_middle = re.compile('.*?([0-9]{3}).*?$')
        r_right = re.compile('^.*?[A-Z]{2}.*?([A-Z]{2}).*?$')

        # Match string
        ret_left = r_left.match(filter_predicted_result.str_plate)
        ret_middle = r_middle.match(filter_predicted_result.str_plate)
        ret_right = r_right.match(filter_predicted_result.str_plate)

        # Plate construction
        filter_predicted_result = ""
        if ret_left or ret_middle or ret_right:
            if ret_left:
                filter_predicted_result += ret_left.group(1)
                filter_predicted_result += "-"
            if ret_middle:
                if not ret_left:
                    filter_predicted_result += "-"
                filter_predicted_result += ret_middle.group(1)
                filter_predicted_result += "-"
            if ret_right:
                if not ret_middle:
                    filter_predicted_result += "-"
                filter_predicted_result += ret_right.group(1)

        # Return processed license plate
        return filter_predicted_result

    @staticmethod
    def get_best_plate(plates):
        # Transform plate object
        list_plates = [plate.str_plate for plate in plates]

        # Remove
        if "PLATE_NOT_FOUND" in list_plates:
            list_plates = list(filter("PLATE_NOT_FOUND".__ne__, list_plates))

        # Plates list to plate dict
        dict_plates = dict([(n, list_plates.count(n)) for n in set(list_plates)])
        return max(dict_plates, key=dict_plates.get)
