import pyautogui
import pydirectinput
import random
import easyocr
import time

from utils import random_sleep, config, mask_only_white, move_mouse_in_x_pattern
import cv2

class skills():
    def __init__(self, reader):
        self.abilities = ['normal' for i in range(len(config['skills']))]
        self.awakening = 'hold'
        self.automove = False
        self.reader = reader
        
    def update(self):
        for i in range(len(self.abilities)):
            if self.is_hold(i):
                self.abilities[i] = 'hold'
            
    def is_hold(self, ability_num):
        self.fetch_image(ability_num)
        image = cv2.imread('./screenshots/curr.png')
        
        pictures = ['hold_skill', 'combo_skill']
        for picture in pictures:
            res = pyautogui.locate(f'./screenshots/{picture}.png', image, confidence=0.65)
            if res:
                return True
        return False
    
    # Saves current image at ./screenshots/cur.png
    def fetch_image(self, ability_num, offset_y=0) -> None:
        box = config['skills'][ability_num]['box']
        region = (box[0], box[3], box[2] - box[0], box[1] - box[3] - offset_y)
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(f'./screenshots/curr.png')
    
    def use_random(self):
        random_skill = random.randint(0, 7)
        cooldown = self.on_cooldown(random_skill)
        
        while cooldown:
            random_skill = random.randint(0, 7)
            cooldown = self.on_cooldown(random_skill)
            random_sleep()
        
        if self.automove:
            pydirectinput.mouseDown(button='left')
            self.automove = False
        
        self.use(random_skill)
        
        move_mouse_in_x_pattern()
    
    def use(self, ability_num):
        
        if self.abilities[ability_num] == 'normal':
            pydirectinput.press(config['skills'][ability_num]['key'])
            random_sleep(0.5)
                
        else:
            pydirectinput.keyDown(config['skills'][ability_num]['key'])
            t1 = time.perf_counter()
            
            while time.perf_counter() - t1 < 2.5:
                random_sleep(0.5)
                
            pydirectinput.keyUp(config['skills'][ability_num]['key'])
    
        pydirectinput.mouseUp(button='left')
        self.automove = True
        random_sleep(0.25)
            
            
    def on_cooldown(self, ability_num):
        self.fetch_image(ability_num, offset_y=10)
        image = mask_only_white(f'./screenshots/curr.png')
        cv2.imwrite('./mask.png', image)
        cooldown = self.reader.readtext(image, allowlist ='0123456789')
        if not cooldown:
            return False
        return True
            
    def use_awakening(self):
        pydirectinput.keyDown('v')
        t1 = time.perf_counter()
        while time.perf_counter() - t1 < 3.5:
            random_sleep(0.5)
        pydirectinput.keyUp('v')
        random_sleep()
    
if __name__ == "__main__":
    skills = skills(easyocr.Reader(['en']))
    skills.update()
    for i in range(30):
        skills.use_random()