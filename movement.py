import pyautogui
import pydirectinput
import time
import random

from utils import random_sleep, config, calculate_blue_coverage, calculate_red_coverage_hsv, find_biggest_red_blob, is_screen_black, find_biggest_blob, adjust_point_to_box
from PIL import ImageGrab

class move():
    def __init__(self, duration=5):
        self.duration = duration
    
    def minimap_locate(self, location):
        x1, y1, x2, y2 = config['minimap_box']
        
        match location:
            case 'portal': pictures = ['portal', 'portalLeft', 'portalRight', 'portalTop', 'portalBot']
            case 'tower': pictures = ['tower', 'towerTop', 'towerBot']
            case 'boss': pictures = ['boss']
        
        if location == 'portal':
            for picture in pictures:
                res = pyautogui.locateOnScreen(f'./screenshots/{picture}.png', confidence=0.8, region=(x1, y2, x2-x1, y1-y2))
                if res:
                    ss = ImageGrab.grab(bbox=(res.left, res.top , res.width + res.left , res.top + res.height))
                    ss.save('./ss.png')
                    if calculate_blue_coverage('./ss.png') >= 45:
                        return res
        elif location == 'tower':
            for picture in pictures:
                res = pyautogui.locateOnScreen(f'./screenshots/{picture}.png', confidence=0.65, region=(x1, y2, x2-x1, y1-y2))
                if res:
                    return res
        elif location == 'boss':
            res = pyautogui.locateOnScreen(f'./screenshots/{pictures[0]}.png', confidence=0.6, region=(x1, y2, x2-x1, y1-y2))
            if res:
                return res
        return None
    
    def minimap_to_game(self, left, top, width, height):
        # Define the coordinates of the destination box on the minimap
        destination_minimap = {'left': left, 'top': top, 'width': width, 'height': height}

        # Calculate the angle between the player and the destination on the minimap
        dest_x = (destination_minimap['left'] + destination_minimap['width'] / 2) - 1675
        dest_y = (destination_minimap['top'] + destination_minimap['height'] / 2) - 165
        
        x_coef = 8.2
        y_coef = 5.684
        
        click_y = y_coef * dest_y
        click_x = x_coef * dest_x
        
        variation = random.randint(-100, 100)
        click_x += variation
        
        click_x, click_y = adjust_point_to_box(click_x, click_y)
            
        return int(click_x), int(click_y)
    
    def adjust_position_randomly(self, x, y):
        variation = random.randint(100, 400)
        if random.randint(0, 1) == 0:
            variation *= -1
        x += variation
        
        variation = random.randint(100, 250)
        if random.randint(0, 1) == 0:
            variation *= -1
        y += variation
        
        pydirectinput.moveTo(x, y, duration=self.duration)
        
        pydirectinput.mouseDown(button='left')
        random_sleep(2)
        pydirectinput.mouseUp(button='left')
    
    def to_portal(self, floor):
        t1 = time.perf_counter()
        while not is_screen_black():
            position = self.minimap_locate('portal')
            if not position:
                continue
            # Change direction
            click_x, click_y = self.minimap_to_game(position.left, position.top, position.width, position.height)
            pydirectinput.moveTo(click_x, click_y, duration=self.duration)
            # Start walking
            pydirectinput.mouseDown(button='left')
            if self.spam_g(5):
                return True
            
            # Stop walking
            pydirectinput.mouseUp(button='left')
            pydirectinput.press('g')
            random_sleep()
            if is_screen_black():
                return True
            
            pos = self.find_portal(floor)
            pydirectinput.click(pos[0], pos[1], button='left')
            if self.spam_g(2.5):
                return True
            
            pydirectinput.press('g')
            
            if time.perf_counter() - t1 > 15:
                return False
        
        return True
    
    def to_tower(self):
        t1 = time.perf_counter()
        tower_fail = 0
        while (time.perf_counter() - t1 < 20 and tower_fail < 3):
            position = self.minimap_locate('tower')
            if not position:
                tower_fail += 1
                random_sleep()
                continue
            # Change direction
            click_x, click_y = self.minimap_to_game(position.left, position.top, position.width, position.height)
            pydirectinput.moveTo(click_x, click_y, duration=self.duration)
            # Start walking
            pydirectinput.mouseDown(button='left')
            
            random_sleep(3.5)
            
            # Stop walking
            pydirectinput.mouseUp(button='left')
            random_sleep(0.25)

            # Move to tower [red blob]
            pos = self.find_tower()
            pydirectinput.click(pos[0], pos[1], button='left')
            random_sleep(1)
            
            pydirectinput.keyDown('c')
            random_sleep(2)
            pydirectinput.keyUp('c')
        
        if tower_fail == 3 and (click_x and click_y):
            self.adjust_position_randomly(click_x, click_y)
        
    
    def to_boss(self):
        t1 = time.perf_counter()
        boss_fail = 0
        while (time.perf_counter() - t1 < 20 and boss_fail < 3):
            position = self.minimap_locate('boss')
            if not position:
                boss_fail += 1
                random_sleep()
                continue
            # Change direction
            click_x, click_y = self.minimap_to_game(position.left, position.top, position.width, position.height)
            pydirectinput.moveTo(click_x, click_y, duration=self.duration)
            # Start walking
            pydirectinput.mouseDown(button='left')
            
            random_sleep(3.5)
            
            # Stop walking
            pydirectinput.mouseUp(button='left')
            random_sleep(0.25)
            
        
    
    def to_point(self, point):
        for i in range(2):
            click_x, click_y = point
            click_x, click_y = adjust_point_to_box(click_x, click_y)
            pydirectinput.moveTo(click_x, click_y, duration=self.duration)
            
            # Start walking
            pydirectinput.mouseDown(button='left')
            random_sleep(3)
            
            # Stop walking
            pydirectinput.mouseUp(button='left')
            random_sleep(1)
        
        return click_x, click_y
            
    def spam_g(self, duration):
        t1 = time.perf_counter()
        while time.perf_counter() - t1 < duration:
            pydirectinput.press('g')
            random_sleep(0.05)
            if is_screen_black():
                return True
        return False
    
    def find_tower(self):
        ss = ImageGrab.grab()
        ss.save('./screenshots/curr.png')
        calculate_red_coverage_hsv('./screenshots/curr.png')
        return find_biggest_red_blob('./screenshots/red_regions.png')
    
    def find_portal(self, floor):
        ss = ImageGrab.grab()
        ss.save('./screenshots/curr.png')
        if floor == 1:
            return find_biggest_blob('./screenshots/curr.png', [100, 140, 50], [110, 200, 130])
        elif floor == 2:
            return find_biggest_blob('./screenshots/curr.png', [100, 140, 10], [130, 255, 50])
        

if __name__ == '__main__':
    mov = move(5)
    print(mov.find_portal(2))
    
        
