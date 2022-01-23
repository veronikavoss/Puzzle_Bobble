from setting import *
from level import *
from start_screen import StartScreen

class Controller:
    def __init__(self,screen,asset):
        self.screen=screen
        self.asset=asset
        self.credit=1
        
        self.start_screen=True
        self.start_screen_sprite=StartScreen(self.screen,self.asset)
        self.playing_game=False
        
        self.font_type='all_font' # all_font, number, alphabet
    
    def set_start_screen_timer(self):
        if self.start_screen_sprite.count_time<=0:
            self.start_screen=False
            self.playing_game=True
    
    def draw_text(self):
        bottom_text=list(f'`````````````````LEVEL-4`````CREDIT`{self.credit:0>2}``')
        for x,text in enumerate(bottom_text):
            if text!='`':
                self.font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][self.font_index]
                self.screen.blit(font,(x*32,32*27))
    
    def update(self):
        self.set_start_screen_timer()
    
    def draw(self):
        if self.start_screen:
            self.start_screen_sprite.draw()
            self.draw_text()
        elif not self.start_screen and self.playing_game:
            self.screen.fill('black')
            self.draw_text()
        # else:
        #     self.screen.fill('black')
        #     self.draw_text()