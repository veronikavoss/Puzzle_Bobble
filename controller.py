from setting import *

class Controller:
    def __init__(self,screen):
        self.screen=screen
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill('white')