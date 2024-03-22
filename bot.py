
from chaos import chaos
from skills import skills
from movement import move
from utils import config
import easyocr
import time
from character_manager import character

class bot():
    def __init__(self):
        self.reader = easyocr.Reader(['en'])
        self.characters = [character(self.reader, i) for i in range(len(config['character_grid']))]
        self.move = move()
        self.skills = skills(self.reader)
        self.chaos = chaos(self.move, self.skills, self.reader)
        
    def run(self, first_char):
        for character in self.characters[first_char:]:
            character.update()
            chaos_level = str(config['character_grid'][character.current_char][2])
            character.check_chaos_aura()
            character.guild_donate()
            while character.available_chaos > 0:
                self.chaos.enter(chaos_level)
                character.available_chaos -= 1
            character.next()
            
if __name__ == "__main__":
    time.sleep(5)
    god = bot()
    god.run(5)