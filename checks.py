import pyautogui
import pydirectinput
from datetime import datetime

from utils import random_sleep, config
from logger import LOGGER

def died():  # get information about wait a few second to revive
    if pyautogui.locateOnScreen("./screenshots/died.png", grayscale=True, confidence=0.9,region=(917, 145, 630, 550)):
        LOGGER.info("Died")
        random_sleep(5)
        while res_ready():
            random_sleep(2)
            pydirectinput.click(x=1275, y=410, button="left")
            random_sleep(2)
        LOGGER.info("Revived")
    return

def res_ready():
    res = pyautogui.locateOnScreen("./screenshots/resReady.png", confidence=0.7,region=(917, 145, 630, 550))
    if not res:
        return False
    return True

def disconnected():
    dc = pyautogui.locateOnScreen("./screenshots/dc.png",region=tuple(config["center_box"]), confidence=0.75)
    ok = pyautogui.locateCenterOnScreen("./screenshots/ok.png", region=tuple(config["center_box"]), confidence=0.75)
    enterServer = pyautogui.locateCenterOnScreen("./screenshots/enterServer.png", confidence=0.75, region=(885, 801, 160, 55))
    if not dc or not ok or not enterServer:
        return False
    currentTime = datetime.now().strftime("%Y%m%d_%H%M%S")
    dc = pyautogui.screenshot()
    dc.save("./debug/dc_" + str(currentTime) + ".png")
    print(
        f"disconnection detected...currentTime : {currentTime} dc:{dc} ok:{ok} enterServer:{enterServer}")
    return True

def heal():
    x = int(config["health_pos"][0] + (870 - config["health_pos"][0]) * config["heal_threshold"])
    y = config["health_pos"][1]
    r1, g, b = pyautogui.pixel(x, y)
    r2, g, b = pyautogui.pixel(x - 2, y)
    r3, g, b = pyautogui.pixel(x + 2, y)
    if not (r1 < 30 or r2 < 30 or r3 < 30):
        return
    LOGGER.info('Healed')
    leaveButton = pyautogui.locateCenterOnScreen("./screenshots/leave.png", grayscale=True, 
                                                    confidence=0.7,region=tuple(config["leaveMenu"]))
    if not leaveButton:
        return
    pydirectinput.press(config["healthPot"])
    return
    
