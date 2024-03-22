import time
import random
import json
import pyautogui
import pydirectinput
import easyocr
import re
from PIL import ImageGrab
import cv2
import numpy as np


with open('config.json', 'r') as f:
    config = json.load(f)

def random_sleep(duration=0.5):
    sleep_coef = config['sleep_coef']
    """
    duration in seconds
    """
    shortest_sleep = duration - duration * sleep_coef
    longest_sleep = duration + duration * sleep_coef
    
    sleep_time = random.uniform(shortest_sleep, longest_sleep)
    time.sleep(sleep_time)

def get_box_center(box):
    center_x = box.left + box.width / 2
    center_y = box.top + box.height / 2
    return int(center_x), int(center_y)

def locate_and_click(image):
    image_pos = pyautogui.locateOnScreen(f"./screenshots/{image}.png", confidence=0.75)
    if not image_pos:
        return False
    center = get_box_center(image_pos)
    pydirectinput.click(x=center[0], y=center[1], button='left')
    random_sleep()
    return True
    
def in_town():
    image_pos = pyautogui.locateOnScreen(f"./screenshots/inTown.png", confidence=0.75)
    if not image_pos:
        return False
    return True

def in_chaos():
    image_pos = pyautogui.locateOnScreen(f"./screenshots/inChaos.png", confidence=0.75)
    if not image_pos:
        return False
    return True

def finished_loading():
    town = pyautogui.locateOnScreen(f"./screenshots/inTown.png", confidence=0.75)
    chaos = pyautogui.locateOnScreen(f"./screenshots/inChaos.png", confidence=0.75)
    
    if chaos or town:
        return True
    return False

def ocr_detect_text(x1, y1, x2, y2, reader):
    """
    x1, y1 - bottom left corner
    x2, y2 - top right corner
    """
    screenshot = ImageGrab.grab(bbox=(x1, y2, x2, y1))
    screenshot.save('./screenshots/curr.png')
    
    res = reader.readtext('./screenshots/curr.png')
    if not res:
        return None
    text = [result[1].replace(' ', '') for result in res]
    return text

def calculate_blue_coverage(image):
    image = cv2.imread(image)
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of blue color in HSV
    lower_blue = np.array([90, 50, 50])  # Lower bound for blue hue
    upper_blue = np.array([130, 255, 255])  # Upper bound for blue hue

    # Create a mask to isolate blue regions
    mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Count the number of blue pixels
    blue_pixel_count = np.count_nonzero(mask)

    # Calculate the total number of pixels in the image
    total_pixels = image.shape[0] * image.shape[1]

    # Calculate the percentage of blue coverage
    blue_coverage_percentage = (blue_pixel_count / total_pixels) * 100

    return blue_coverage_percentage

def calculate_red_coverage_hsv(image):
    image = cv2.imread(image)
    # Convert image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


    # Define range of red color in HSV (additional range for red hue that wraps around)
    lowest_red_wrap = np.array([175, 50, 50])     # Lower bound for red hue
    highest_red_wrap = np.array([180, 255, 255])  # Upper bound for red hue

    # Create a mask to isolate red regions
    mask = cv2.inRange(hsv_image, lowest_red_wrap, highest_red_wrap)
    
    red_regions = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('./screenshots/red_regions.png', red_regions)

    # Count the number of red pixels
    red_pixel_count = np.count_nonzero(mask)

    # Calculate the total number of pixels in the image
    total_pixels = image.shape[0] * image.shape[1]

    # Calculate the percentage of red coverage
    red_coverage_percentage = (red_pixel_count / total_pixels) * 100

    return red_coverage_percentage

def find_biggest_red_blob(masked_image):
    masked_image = cv2.imread(masked_image)
    # Convert the masked image to grayscale
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)

    # Find contours in the masked image
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours found, return None
    if not contours:
        return None

    # Find the contour with the maximum area
    max_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Return the coordinates of the bounding box
    x_center = int(x + w / 2)
    y_center = int(y + h / 2)
    x_center, y_center = adjust_point_to_box(x_center, y_center)
    return (x_center, y_center)

def find_biggest_blob(image, color_lower, color_upper):
    image = cv2.imread(image)
    # Convert the masked image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds for the dark blue color
    lower_blue = np.array(color_lower)
    upper_blue = np.array(color_upper)

    # Create a mask for pixels within the specified color range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_regions = cv2.bitwise_and(image, image, mask=mask)
    cv2.imwrite('./screenshots/blue.png', blue_regions)

    # Find contours in the masked image
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If no contours found, return None
    if not contours:
        return None

    # Find the contour with the maximum area
    max_contour = max(contours, key=cv2.contourArea)

    # Get the bounding box of the largest contour
    x, y, w, h = cv2.boundingRect(max_contour)

    # Return the coordinates of the bounding box
    x_center = int(x + w / 2)
    y_center = int(y + h / 2)
    
    x_center, y_center = adjust_point_to_box(x_center, y_center)
    return (x_center, y_center)

def mask_only_white(image_path, tolerance=100):
    # Load the image
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Unable to load the image.")
        return None

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for white color in HSV
    lower_white = np.array([0, 0, 255 - tolerance])
    upper_white = np.array([255, tolerance, 255])

    # Create a mask to only select white pixels
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Apply the mask to the original image
    result = cv2.bitwise_and(image, image, mask=mask)
    return result

def allow_only_numbers(input_string):
    # Use regular expression to find all numbers in the string
    numbers = re.findall(r'\d+', input_string)
    # Join the numbers into a single string
    numbers_string = ''.join(numbers)
    return numbers_string

def count_pixels_with_color(pos, target_color):
    # Capture the screen image
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Extract the region of interest (ROI) from the screenshot based on the provided position
    x = pos[0]
    y = pos[3]
    width = pos[2] - pos[0]
    height = pos[1] - pos[3]
    roi = screenshot[y:y+height, x:x+width]
    
    if roi.size == 0:
        return 0, None

    target_color_bgr = (target_color[2], target_color[1], target_color[0])
    # Convert the target color to a NumPy array for comparison
    target_color_bgr = np.array(target_color_bgr)

    # Create a mask to detect pixels with the target color
    mask = cv2.inRange(roi, target_color_bgr, target_color_bgr)

    # Count the number of pixels with the target color
    pixel_count = cv2.countNonZero(mask)

    # Find the position of one of the pixels with the target color
    if pixel_count > 0:
        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Get the bounding box of the largest contour
        x, y, w, h = cv2.boundingRect(contours[0])
        # Adjust the position by adding the coordinates of the top-left corner of the ROI
        pixel_pos = (x + pos[0], y + pos[3])
    else:
        pixel_pos = None

    return pixel_count, pixel_pos

def move_mouse_in_x_pattern():
    # Get current mouse position
    current_x, current_y = pydirectinput.position()

    # Calculate the displacement from the center
    dx = current_x - 960
    dy = current_y - 540
    
    # Determine the quadrant
    if dx >= 0 and dy >= 0:
        # Bottom right quadrant
        new_x = 700
        new_y = 300
    elif dx >= 0 and dy < 0:
        # Top right quadrant
        new_x = 1250
        new_y = 700
    elif dx < 0 and dy >= 0:
        # Bottom left quadrant
        new_x = 1250
        new_y = 300
    else:
        # Top left quadrant
        new_x = 700
        new_y = 700

    # Move the mouse to the new position
    pydirectinput.moveTo(new_x, new_y, duration=0.3)

def is_screen_black(threshold=0.8):
    # Capture a screenshot of the entire screen
    screenshot = ImageGrab.grab()

    # Convert the screenshot to grayscale
    grayscale_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

    # Calculate the total number of pixels
    total_pixels = grayscale_image.shape[0] * grayscale_image.shape[1]

    # Calculate the number of black pixels
    num_black_pixels = np.sum(grayscale_image < 10)  # Assuming black if pixel intensity is below 10

    # Calculate the percentage of black pixels
    black_pixel_percentage = num_black_pixels / total_pixels

    # Check if the percentage exceeds the threshold
    if black_pixel_percentage > threshold:
        return True
    else:
        return False
    
def is_boss_bar():
    image_pos = pyautogui.locateOnScreen(f"./screenshots/bossBar.png", confidence=0.75)
    if not image_pos:
        return False
    return True

def adjust_point_to_box(x, y):
    """
    Adjust the point (x, y) to be within the bounding box defined by (x1, y1) and (x2, y2).
    (x1, y1) is the bottom-left corner and (x2, y2) is the top-right corner.
    """
    x1, y1, x2, y2 = tuple(config['usable_area_box'])
    # Ensure x is within the bounds
    if x < x1:
        x = x1
    elif x > x2:
        x = x2

    # Ensure y is within the bounds
    if y < y2:
        y = y2
    elif y > y1:
        y = y1

    return x, y
    
    
if __name__ == '__main__':
    time.sleep(3)
    map_pos = tuple(config['minimap_box'])
    color = tuple(config['monsters_color'])
    pixel_count, pos = count_pixels_with_color(map_pos, color)
    print(pixel_count)