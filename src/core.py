import argparse as argparse
import logging
import time
from pathlib import Path

import cv2
import imutils
import numpy as np

import displayplate
import mock
import ocr
import ocrposttreatment
import ocrpretreatment
from ocrutils import OcrUtils
from plate import Plate

if not OcrUtils.is_windows():
    import cameracsi

# MAIN
if __name__ == "__main__" or "core":
    # Arg parser
    parser = argparse.ArgumentParser(description="ocr_JI3-700")
    parser.add_argument("-v", "--verbose", action="store_true", default=True, help="Enable verbose mode")
    parser.add_argument("-q", "--quiet", action="store_true", default=False, help="Enable quiet mode")
    parser.add_argument("-d", "--debug_picture", action="store_true", default=False,
                        help="Enable debug display picture")
    parser.add_argument("-s", "--save_picture", action="store_true", default=True, help="Enable debug save picture")
    parser.add_argument("-i", "--input", type=str, default="RASPBERRY_CAMERA", choices=["MOCK", "RASPBERRY_CAMERA"])
    parser.add_argument("-p", "--mock_path", type=str, default="/../data/dataset_1",
                        help="Input directory mock path with inside picture license plate and plate name like AA-666-BB.jpg")
    parser.add_argument("-t", "--process_time", action="store_true", default=True,
                        help="Enable process time calculator")
    args = parser.parse_args()

    # Define global arg variables
    ARG_VERBOSE = args.verbose
    ARG_QUIET = args.quiet
    ARG_DEBUG = args.debug_picture
    ARG_SAVE = args.save_picture
    if args.input == "RASPBERRY_CAMERA":
        ARG_INPUT = OcrUtils.InputMode.RASPBERRY_CAMERA
    else:
        ARG_INPUT = OcrUtils.InputMode.MOCK
    ARG_MOCK_PATH = args.mock_path
    ARG_PROCESS_TIME = args.process_time

    # Define process time
    if ARG_PROCESS_TIME:
        time_start = time.time()

    # Define logger
    if ARG_VERBOSE and ARG_QUIET:
        raise ValueError("You can't set 'ARG_VERBOSE' and 'ARG_QUIET' parameter!")

    level_log = logging.INFO
    if ARG_VERBOSE:
        level_log = logging.DEBUG
    if ARG_QUIET:
        level_log = logging.ERROR

    # Create log path
    Path("log").mkdir(parents=True, exist_ok=True)

    # Create save path
    if ARG_SAVE:
        Path("tmp").mkdir(parents=True, exist_ok=True)

    # Generate log file name with timestamp
    log_path_name = "log/logger_" + time.strftime("%Y-%m-%d_%H-%M-%S") + ".log"

    # Create logger with 'spam_application'
    logger = logging.getLogger('Core')
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(level_log)

    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_path_name)
    fh.setLevel(level_log)

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level_log)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s - [%(name)s] - [%(levelname)s] - %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    # Define global vars
    KERNEL = np.ones((2, 2), np.uint8)

    # Instantiate class
    OCR_POST_TREATMENT = ocrposttreatment.PostTreatment()
    OCR_PRE_TREATMENT = ocrpretreatment.PreTreatment(ARG_DEBUG)
    DISPLAY = displayplate.DisplayPlate(ARG_DEBUG)
    OCR = ocr.Ocr()

    # Define and get picture by camera or mock
    if ARG_INPUT is OcrUtils.InputMode.RASPBERRY_CAMERA:
        CAMERACSI = cameracsi.RaspberryCsiCamera()
        frames = CAMERACSI.get_snapshots(10)
    else:
        MOCK = mock.Mock(ARG_MOCK_PATH)
        list_license_plates, frames = MOCK.get_frames()

    # Define main vars
    one_plate_is_found = False
    predicted_license_plates = []
    predicted_license_plates_filtered = []
    for i, frame in enumerate(frames):
        if ARG_INPUT is OcrUtils.InputMode.RASPBERRY_CAMERA:
            logger.info("Frame number: {}".format(i))
        else:
            logger.info("[Core] Frame number: {} - named: '{}'".format(i, list_license_plates[i].str_plate))

        # Display picture
        DISPLAY.debug_display_picture("frame", frame, 0)

        # Resize
        logger.debug("Resize frame")
        frame = cv2.resize(frame, (640, 480))

        # Find lines
        # Grey convert
        logger.debug("Grey convert")
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert to grey scale
        DISPLAY.debug_display_picture("gray", gray, 0)

        # Bilateral filter -> smoothing
        logger.debug("Bilateral filter")
        gray = cv2.bilateralFilter(gray, 13, 15, 15)
        DISPLAY.debug_display_picture("bilateralFilter", gray, 0)

        # Canny filter -> detect outlines
        logger.debug("Canny filter")
        edged = cv2.Canny(gray, 30, 200)
        DISPLAY.debug_display_picture("Canny", edged, 0)

        # Get contours
        logger.debug("Get contours")
        contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        screenCnt = None
        plate_is_found = False
        for c in contours:
            # Approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4:
                plate_is_found = True
                screenCnt = approx
                break

        if plate_is_found:
            one_plate_is_found = True
            logger.info("plate_is_found")

            # Calculate mask
            logger.debug("Calculate mask")
            mask = np.zeros(gray.shape, np.uint8)
            cv2.drawContours(mask, [screenCnt], 0, 255, -1, )
            new_image = cv2.bitwise_and(frame, frame, mask=mask)
            DISPLAY.debug_display_picture("new_image", new_image, 0)

            # Debug - Display all contours
            debug_picture = frame.copy()
            # Draw contours
            logger.debug("drawContours: contours")
            cv2.drawContours(debug_picture, [screenCnt], -1, (0, 0, 255), 2)
            # Draw points
            logger.debug("drawContours: points")
            cv2.drawContours(debug_picture, screenCnt, -1, (0, 255, 0), 8)
            DISPLAY.debug_display_picture("Display all contours", debug_picture, 0)

            # Character segmentation
            # Crop
            logger.info("Character segmentation")
            logger.debug("Crop frame")
            (x, y) = np.where(mask == 255)
            (top_x, top_y) = (np.min(x), np.min(y))
            (bottom_x, bottom_y) = (np.max(x), np.max(y))
            cropped = gray[top_x:bottom_x + 1, top_y:bottom_y + 1]
            DISPLAY.debug_display_picture("cropped", cropped, 0)

            # Pretreatment before character recognition
            cropped_with_pretreatments = cropped

            # Get rotation
            cropped_with_pretreatments, debug_picture = OCR_PRE_TREATMENT.get_best_rotation(screenCnt,
                                                                                            cropped_with_pretreatments,
                                                                                            debug_picture)

            # Binarization with thresholding
            logger.debug("Binarization with OTSU threshold")
            _, cropped_with_pretreatments = cv2.threshold(cropped_with_pretreatments, 125, 255,
                                                          cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            # Remove noise
            # Open
            logger.info("Open plate")
            # Erode
            logger.debug("Erode")
            cropped_with_pretreatments = cv2.erode(cropped_with_pretreatments, KERNEL, iterations=1)
            # Dilate
            logger.debug("Dilate")
            cropped_with_pretreatments = cv2.dilate(cropped_with_pretreatments, KERNEL, iterations=1)
            DISPLAY.debug_display_picture("Open", cropped_with_pretreatments, 0)

            # Close
            logger.info("Close plate")
            # Dilate
            logger.debug("Dilate")
            cropped_with_pretreatments = cv2.dilate(cropped_with_pretreatments, KERNEL, iterations=1)
            # Erode
            logger.debug("Erode")
            cropped_with_pretreatments = cv2.erode(cropped_with_pretreatments, KERNEL, iterations=1)
            DISPLAY.debug_display_picture("Open", cropped_with_pretreatments, 0)

            # Prediction
            logger.info("Prediction is in running")
            predicted_result = Plate(OCR.ocr_prediction(cropped_with_pretreatments))

            # Post treatment
            logger.info("Post treatment")
            # Replace and concatenate for clean up
            logger.debug("split and replace")
            predicted_result.split()
            filter_predicted_result = Plate(predicted_result.str_plate.replace("\n", ""))

            # Regex
            logger.debug("Apply regex")
            filter_predicted_result.str_plate = OCR_POST_TREATMENT.regex_plate(filter_predicted_result)
        else:
            logger.info("PLATE_NOT_FOUND")
            predicted_result = Plate("PLATE_NOT_FOUND")
            filter_predicted_result = Plate("PLATE_NOT_FOUND")

        # Append lists for benchmark and display
        logger.debug("predicted_result: '{}'".format(predicted_result.str_plate))
        predicted_license_plates.append(predicted_result)
        logger.debug("filter_predicted_result: '{}'".format(filter_predicted_result.str_plate))
        predicted_license_plates_filtered.append(filter_predicted_result)

        # Generate dashboard frame
        logger.debug("Generate dashboard frame")
        dashboard_frame = cv2.resize(debug_picture, (1280, 720))
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 1
        color = (0, 0, 255)
        thickness = 2
        dashboard_frame = cv2.putText(dashboard_frame, "predicted_result: '" + predicted_result.str_plate + "'",
                                      (50, 50), font, fontScale, color, thickness,
                                      cv2.LINE_AA)
        dashboard_frame = cv2.putText(dashboard_frame,
                                      "filter_predicted_result: '" + filter_predicted_result.str_plate + "'", (50, 100),
                                      font, fontScale, color, thickness,
                                      cv2.LINE_AA)
        DISPLAY.debug_display_picture("dashboard_frame", dashboard_frame, 0)
        if ARG_SAVE:
            if ARG_INPUT is OcrUtils.InputMode.RASPBERRY_CAMERA:
                str_path = "tmp/{}-dashboard.png".format(i)
            else:
                str_path = "tmp/{}-dashboard.png".format(list_license_plates[i].str_plate)
            cv2.imwrite(str_path, dashboard_frame)
        DISPLAY.debug_display_picture("resize", dashboard_frame, 0)

    # Benchmark and display frames
    logger.info("Benchmark and display")
    if ARG_INPUT is OcrUtils.InputMode.RASPBERRY_CAMERA:
        DISPLAY.display_predicted(predicted_license_plates, predicted_license_plates_filtered)
    else:
        DISPLAY.calculate_predicted_accuracy(list_license_plates, predicted_license_plates,
                                             predicted_license_plates_filtered)

    # Get best plate
    if one_plate_is_found:
        logger.debug("get_best_plate is in running")
        best_plate = ocrposttreatment.PostTreatment.get_best_plate(predicted_license_plates_filtered)
        logger.info("best_plate: '{}'".format(best_plate))
    else:
        logger.info("best_plate: 'PLATE_NOT_FOUND'")

    # Calculate and display process time
    if ARG_PROCESS_TIME:
        time_stop = time.time()
        logger.info("Process time: {} second(s).".format((time_stop - time_start)))
