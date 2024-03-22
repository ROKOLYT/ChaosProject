import pyautogui
import pydirectinput

from utils import random_sleep, is_screen_black, config

def game_menu_active():
    menu = pyautogui.locateOnScreen("./screenshots/gameMenuFull.png", confidence=config['ocr_confidence'])
    if menu:
        return True
    return False

def guild_menu_active():
    menu1 = pyautogui.locateCenterOnScreen('./screenshots/guild_donate.png', confidence=0.75)
    menu2 = pyautogui.locateOnScreen('./screenshots/ok.png', confidence=0.75)
    if menu1 or menu2:
        return True
    return False

def integrated_dungon_active():
    menu = pyautogui.locateOnScreen("./screenshots/integrated_dungeon.png", confidence=config['ocr_confidence'])
    if menu:
        return True
    return False

def open_integrated_dungeon():
    pydirectinput.keyDown('alt')
    random_sleep()
    pydirectinput.press('q')
    random_sleep()
    pydirectinput.keyUp('alt')
    
def enter_chaos_menu():
    pydirectinput.click(x=700, y=430, button='left')
    random_sleep()
    pydirectinput.click(x=1215, y=730, button='left')
    random_sleep()
    pydirectinput.click(x=1480, y=305, button='left')
    random_sleep()

def select_chaos_level(level):
    chaos = config['chaos_levels_pos'][str(level)]
    pydirectinput.click(x=chaos[0][0], y=chaos[0][1], button='left')
    random_sleep()
    pydirectinput.click(x=chaos[1][0], y=chaos[1][1], button='left')
    random_sleep()
    
def enter_chaos_confirm():
    # Press the "Enter" button and confirm
    pydirectinput.click(x=1390, y=785, button='left')
    random_sleep()
    pydirectinput.click(x=925, y=590, button='left')
    random_sleep()
    
def enter_chaos(level):
    open_integrated_dungeon()
    if not integrated_dungon_active():
        open_integrated_dungeon()
    
    enter_chaos_menu()
    select_chaos_level(level)
    enter_chaos_confirm()
    
    random_sleep(6)
    while is_screen_black(0.6):
        random_sleep(2)

def leave_chaos(finished=False):
    if finished:
        pydirectinput.click(x=960, y=850, button='left')
        random_sleep(1)
    
    pydirectinput.click(x=155, y=350, button='left')
    random_sleep()
    pydirectinput.click(x=925, y=580, button='left')
    random_sleep(15)
