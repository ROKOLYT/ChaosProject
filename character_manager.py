import pyautogui as pg
import pydirectinput
import easyocr

pydirectinput.PAUSE = 0.05
from utils import random_sleep, locate_and_click, finished_loading, ocr_detect_text, config
from gui_navigator import game_menu_active, guild_menu_active
from logger import LOGGER

class character():
    def __init__(self, reader, character_num=0):
        self.current_char = character_num
        self.available_chaos = 1
        self.reader = reader
        
    def close_menu(self):
        while game_menu_active():
                pydirectinput.press('esc')
                random_sleep()
        
    def open_menu(self):
        self.close_menu()
            
        pydirectinput.press('esc')
        random_sleep()
        
        pydirectinput.click(x=config['switch_character_point'][0], y=config['switch_character_point'][1], button='left')
        random_sleep()
    
    def connect_available(self):
        pixel = pg.pixel(x=config['connect_to_char_point'][0], y=config['connect_to_char_point'][1])
        if list(pixel) != config['connect_to_char_available_rgb']:
            return False
        return True
    
    def update(self):
        self.open_menu()
        
        for i, char in enumerate(config['character_grid']):
            # Select character
            pydirectinput.click(x=char[0], y=char[1], button='left')
            
            random_sleep(1)
            
            # Check for possible connection
            if not self.connect_available():
                self.current_char = i
                
                # Exit menu
                self.close_menu()
                    
                return
    
    def next(self):
        self.open_menu()
        
        if self.current_char + 1 >= len(config['character_grid']):
            self.close_menu()
            return
        
        char = config['character_grid'][self.current_char + 1]
        pydirectinput.click(x=char[0], y=char[1], button='left')
        random_sleep()
        
        if not self.connect_available():
            self.close_menu()
            return
        
        # Connect
        pydirectinput.click(x=config['connect_to_char_point'][0], y=config['connect_to_char_point'][1], button='left')
        random_sleep()
        
        # Confirm
        locate_and_click('ok')
        random_sleep(5)
        
        while not finished_loading():
            random_sleep(2)
            
        random_sleep()
        pydirectinput.click(x=960, y=540, button='left')
        LOGGER.info('Finished loading')
        
    def check_chaos_aura(self):
        self.open_menu()
        
        box = config['chaos_daily_box']
        random_sleep(1.5)
        res = ocr_detect_text(x1=box[0], y1=box[1], x2=box[2], y2=box[3], reader=self.reader)
        
        if not res:
            self.close_menu()
            return

        if '100' in res[0]:
            self.available_chaos = 2
        elif '5050' in res[0] or '50/50' in res[0]:
            self.available_chaos = 1
        else:
            self.available_chaos = 0
        
        self.close_menu()
    
    def guild_donate(self):
        pydirectinput.keyDown('alt')
        random_sleep()
        pydirectinput.press('u')
        random_sleep()
        pydirectinput.keyUp('alt')
        while not locate_and_click('guild_donate'):
            random_sleep()
        random_sleep()
        
        donate = config['guild_donate_silver_point']
        pydirectinput.click(x=donate[0], y=donate[1], button='left')
        random_sleep()
        
        while guild_menu_active():
            pydirectinput.press('esc')
            random_sleep()
            
            
            
            
if __name__ == '__main__':
    char = character(easyocr.Reader(['en']), 0)
    char.update()
    char.check_chaos_aura()
    print(char.available_chaos)
        
        
            
        
        