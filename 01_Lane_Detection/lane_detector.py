import cv2
import numpy as np


class LaneDetector:

    def __init__(self):

        pass

    def grayscale(self, image):

        return cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )
    
    def blur(self, image):

        return cv2.GaussianBlur(
            image,
            (5,5),
            0
        )

    def canny(self, image):

        return cv2.Canny(
            image,
            30,
            100
        )
    
    def region_of_interest(self, image):

        height = image.shape[0]
        width = image.shape[1]

        polygon = np.array([
        [
            (200, height),
            (550, 450),
            (850, 450),
            (width, height-100),
            (width, height)
        ]
        ])

        mask = np.zeros_like(image)

        cv2.fillPoly(
            mask,
            polygon,
            255
        )

        cropped = cv2.bitwise_and(
            image,
            mask
        )

        return cropped
    
    def detect_lines(self, image):

        lines = cv2.HoughLinesP(
            image,
            rho=2,
            theta=np.pi/180,
            threshold=100,
            minLineLength=40,
            maxLineGap=5
        )

        return lines
    
    def draw_lines(self, image, lines):

        line_image = np.zeros_like(image)

        if lines is None:
            return line_image

        for line in lines:

            x1, y1, x2, y2 = line[0]

            cv2.line(
                line_image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

        return line_image
    
    def classify_lines(self, lines):

        left_lines = []
        right_lines = []

        if lines is None:
            return left_lines, right_lines

        for line in lines:

            x1, y1, x2, y2 = line[0]

            if x1 == x2:
                continue

            slope = (y2 - y1) / (x2 - x1)

            if slope < 0:
                left_lines.append(line[0])

            else:
                right_lines.append(line[0])

        return left_lines, right_lines
    
    def average_lines(self, left_lines, right_lines):

        left_fit = []
        right_fit = []

        for line in left_lines:

            x1, y1, x2, y2 = line

            fit = np.polyfit(
                (x1, x2),
                (y1, y2),
                1
            )

            left_fit.append(fit)

        for line in right_lines:

            x1, y1, x2, y2 = line

            fit = np.polyfit(
                (x1, x2),
                (y1, y2),
                1
            )

            right_fit.append(fit)

        left_avg = np.average(
            left_fit,
            axis=0
        )

        right_avg = np.average(
            right_fit,
            axis=0
        )

        return left_avg, right_avg

    def make_coordinates(self, image, line_parameters):

        slope, intercept = line_parameters

        y1 = image.shape[0]
        y2 = int(y1 * 0.6)

        x1 = int((y1 - intercept) / slope)
        x2 = int((y2 - intercept) / slope)

        return np.array([
            x1,
            y1,
            x2,
            y2
        ])
    
    def draw_lane_lines(self, image, left_line, right_line):

        line_image = np.zeros_like(image)

        cv2.line(
            line_image,
            (left_line[0], left_line[1]),
            (left_line[2], left_line[3]),
            (255, 0, 0),
            8
        )

        cv2.line(
            line_image,
            (right_line[0], right_line[1]),
            (right_line[2], right_line[3]),
            (0, 255, 0),
            8
        )

        return line_image

