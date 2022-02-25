import logging

import cv2


class DisplayPlate:
    def __init__(self, DEBUG_DISPLAY_PICTURES):
        # Get logger
        self.logger = logging.getLogger("Core.Display")
        self.logger.debug("Constructor called, DisplayPlate instantiated.")

        self.DEBUG_DISPLAY_PICTURES = DEBUG_DISPLAY_PICTURES

    def display_predicted(self, predicted_list, predicted_license_plates_filtered):
        """
        @staticmethod
        This method display all results by camera.

        :param predicted_list: list predicted by OCR
        :param predicted_license_plates_filtered: list predicted by OCR + post treatment

        :return void
        """
        self.logger.info("-----------------------------------------------------------")
        self.logger.info("Predicted License Plate    Predicted License Plate Filtered")
        self.logger.info("-----------------------   ---------------------------------")

        for predict_plate, predict_plate_filtered in zip(predicted_list, predicted_license_plates_filtered):
            self.logger.info("'{}'                        '{}'                ".format(predict_plate.str_plate, predict_plate_filtered.str_plate))

    def calculate_predicted_accuracy(self, actual_list, predicted_list, predicted_license_plates_filtered):
        """
        @staticmethod
        This method display all results of OCR with benchmark values.

        :param actual_list: list of real plate
        :param predicted_list: list predicted by OCR
        :param predicted_license_plates_filtered: list predicted by OCR + post treatment

        :return void
        """
        self.logger.info(
            "-----------------------------------------------------------------------------------------------")
        self.logger.info(
            "Actual License Plate    Predicted License Plate    Predicted License Plate Filtered    Accuracy")
        self.logger.info(
            "--------------------    -----------------------    --------------------------------    --------")

        accuracys = []
        for actual_plate, predict_plate, predict_plate_filtered in zip(actual_list, predicted_list,
                                                                       predicted_license_plates_filtered):
            accuracy = "0"
            num_matches = 0
            if actual_plate.str_plate == predict_plate_filtered.str_plate:
                accuracy = "100"
            else:
                if len(actual_plate.str_plate) == len(predict_plate_filtered.str_plate):
                    for a, p in zip(actual_plate.str_plate, predict_plate_filtered.str_plate):
                        if a == p:
                            num_matches += 1
                    accuracy = str(round((num_matches / len(actual_plate.str_plate)), 2) * 100)

            accuracys.append(accuracy)
            accuracy += " %"

            self.logger.info(
                "    '{}'              '{}'                  '{}'                      '{}'".format(actual_plate.str_plate,
                                                                                                   predict_plate.str_plate,
                                                                                                   predict_plate_filtered.str_plate,
                                                                                                   accuracy))

        # Calculate global precision
        global_accuracy = round(sum(float(accuracy) for accuracy in accuracys) / len(actual_list), 2)
        self.logger.info("                                ---> Global precision: {} % <---".format(global_accuracy))

    def debug_display_picture(self, name, picture, waitkey):
        """
        This method is used for display picture when DEBUG_DISPLAY_PICTURES is enabled in core.

        :param name: windows name
        :param picture: picture matrice
        :param waitkey: 0 for push to next and greater than 0 for wait in milliseconds

        :return void
        """
        if self.DEBUG_DISPLAY_PICTURES:
            cv2.imshow(name, picture)
            cv2.waitKey(waitkey)
