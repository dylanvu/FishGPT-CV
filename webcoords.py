import cv2
import numpy as np

# GamePlan
# Read From WebCam
# Apply Coordinates to the Video Received
    # Apply Question Coordinates
    # Can Be Scalable to how many questions/answers
# Mask Out all the colors, Recognize Goldfish Color
# Get Coordinates From Color
# Check which Coordinate Matches From Color, Return Answer

# Input Coordinates, Returns if it is in the Quadrant Parameter 
def CheckCoordinate(X: int, Y: int, Quadrants: list):
    return False

# Apply Question & Emoji To Quadrant
def QuestionQuadrants(Questions: list, Emojis: list, Quadrants: list):
    return False

# Function To Get Colors
def get_limits(color):
    c = np.uint8([[color]])  # BGR values
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)

    hue = hsvC[0][0][0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit