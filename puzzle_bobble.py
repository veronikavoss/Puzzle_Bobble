from asset import Asset
from controller import Controller
from setting import *

class PuzzleBobble:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(title)
        self.screen=pygame.display.set_mode(screen_size)
        self.clock=pygame.time.Clock()
        self.asset=Asset()
        self.running=True
        self.start()
    
    def start(self):
        self.controller=Controller(self.screen,self.asset)
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
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    self.controller.credit+=1
                    self.controller.level+=1
                if self.controller.start_screen:
                    if event.key==pygame.K_SPACE:
                        self.controller.start_screen=False
                        self.controller.playing_game=True
    
    def update(self):
        self.controller.update()
    
    def draw(self):
        self.controller.draw()

PuzzleBobble()
pygame.quit()