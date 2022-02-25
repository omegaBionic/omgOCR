import logging
import time

import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray


class RaspberryCsiCamera:
    def __init__(self, resolution=(640, 480)):
        # Get logger
        self.logger = logging.getLogger("Core.RaspberryCsiCamera")
        self.logger.debug("Constructor called, RaspberryCsiCamera instantiated.")

        # Variables
        self.resolution = resolution
        self._is_running = None
        self._grabber = None
        self.picture = None

        # CSI camera connection
        self.logger.debug("CSI camera connection.")
        self.camera = PiCamera()

        self.camera.resolution = self.resolution
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=self.resolution)

        # Allow the camera to warmup
        time.sleep(0.1)

        self.logger.debug("Constructor done.")

    def __del__(self):
        self.camera.stop_preview()

    def get_snapshots(self, number_of_snapshot):
        # self.camera.start_preview()
        self.logger.info("get_snapshots is running.")
        self.logger.info("Get {} frames.".format(number_of_snapshot))
        frames = []
        # capture frames from the camera
        for i, frame in enumerate(self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)):
            # Grab the raw NumPy array representing the image, then initialize the timestamp
            image = frame.array

            # Append frame list
            frames.append(image)

            # Clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if i > number_of_snapshot:
                break
        return frames

    def display_camera(self):
        self.logger.info("display_camera is running.")
        # Cannot be used if grabber is enabled
        if self.is_running:
            raise self.logger.error("Cannot be used if grabber is enabled.")

        # capture frames from the camera
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # Grab the raw NumPy array representing the image, then initialize the timestamp
            image = frame.array

            # Show the frame
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

            # Clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break
