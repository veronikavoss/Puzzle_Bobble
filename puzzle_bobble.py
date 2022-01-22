from controller import Controller
from setting import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen=pygame.display.set_mode(screen_size)
        self.clock=pygame.time.Clock()
        self.running=True
        self.start()
    
    def start(self):
        self.controller=Controller(self.screen)
        self.loop()
    
    def loop(self):
        while self.running:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()
            pygame.display.update()
    
    def event(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.running=False
    
    def update(self):
        self.controller.update()
    
    def draw(self):
        self.controller.draw()
puzzle_bobble=Game()
pygame.quit()