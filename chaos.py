from checks import died, heal, disconnected
from utils import is_screen_black, random_sleep, is_boss_bar, in_town, config, ocr_detect_text, allow_only_numbers, count_pixels_with_color
from gui_navigator import enter_chaos, leave_chaos
import pydirectinput
import pyautogui
import time
from PIL import ImageGrab
from movement import move

from logger import LOGGER

class chaos():
    def __init__(self, move, skills, reader):
        self.floor = 1
        self.move = move
        self.skills = skills
        self.fail_safe_time = 0
        self.fail_safe_monsters = 0
        self.reader = reader
        self.t1 = time.perf_counter()
        self.walking = 0
    
    def finished(self):
        res = pyautogui.locateOnScreen('./screenshots/chaos_finished.png', confidence=0.8)
        if not res:
            return False
        return True
        
    def clear(self, floor=1):
        self.fail_safe_time = 0
        random_sleep()
        self.skills.update()
        self.floor = floor
        pydirectinput.press('z')
        while True:
            self.safety_checks()
            if self.floor in [1, 2]:
                self.portal()
                
            if self.floor == 3:
                self.tower()
                self.monsters()
            
            # Check for boss and monsters
            self.boss()
                    
            if is_screen_black():
                LOGGER.warning('Acidentally entered portal')
                LOGGER.info(f'Floor {self.floor}')
                self.floor += 1
            
            self.skills.use_random()
            
            if self.finished():
                leave_chaos(finished=True)
                while not in_town():
                    random_sleep(2)
                break
            
            if self.time_left() <= 20:
                if self.fail_safe_time < 3:
                    self.fail_safe_time += 1
                    continue
                leave_chaos()
                while not in_town():
                    random_sleep(2)
                break
            else:
                self.fail_safe_time = 0
    
    def time_left(self):
        pos = config['chaos_time_box']
        res = ocr_detect_text(pos[0], pos[1], pos[2], pos[3], self.reader)
        if not res:
            return 0.0
        res = allow_only_numbers(res[0])
        if res:
            return int(res)
        return 0.0
    
    def safety_checks(self):
        if self.floor > 3:
            self.floor = 3
        died()
        heal()
        if disconnected():
            raise KeyboardInterrupt
        
    def portal(self):
        portal = self.move.minimap_locate('portal')
        if portal:
            LOGGER.info('Moving to portal')
            floor = self.move.to_portal(self.floor)
            if not floor:
                return
            
            self.floor += 1
            LOGGER.info(f'Floor {self.floor}')
            random_sleep(10)
    
    def tower(self):
        tower = self.move.minimap_locate('tower')
        if tower:
            LOGGER.info('Moving to tower')
            self.move.to_tower()
            
    def monsters(self):
        monsters, pos = self.monsters_present()
        if not monsters:
            return
        monster_pos = self.move.minimap_to_game(pos[0], pos[1], 2, 2)
        x, y = self.move.to_point(monster_pos)
        self.walking += 1
        if self.walking % 3 == 0:
            self.move.adjust_position_randomly(x, y)
    
    def boss(self):
        boss = self.move.minimap_locate('boss')
        if (boss and not is_boss_bar()) or (is_boss_bar() and time.perf_counter() - self.t1 > 20):
            self.t1 = time.perf_counter()
            self.floor = 2
            LOGGER.info('Moving to boss')
            self.move.to_boss()
            self.skills.use_awakening()
        if is_boss_bar():
            self.floor = 2
            
    def monsters_present(self):
        map_pos = tuple(config['minimap_box'])
        color = tuple(config['monsters_color'])
        pixel_count, pos = count_pixels_with_color(map_pos, color)
        
        if pixel_count > 10 and self.fail_safe_monsters < 10:
            self.fail_safe_monsters += 1
            return False, pos
        elif pixel_count > 10:
            LOGGER.info('Moving to monster')
            return True, pos
        else:
            self.fail_safe_monsters = 0
            return False, pos
                
    def enter(self, level):
        enter_chaos(level)
        self.clear()
        return

if __name__ == '__main__':
    chao = chaos(move(), 1, 1)
    res = chao.monsters()

            
            
            