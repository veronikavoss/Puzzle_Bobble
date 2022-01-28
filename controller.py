from setting import *
from start_screen import StartScreen
from launcher import Launcher
from level import *
from bubble import Bubble

class Controller:
    def __init__(self,screen,asset):
        self.screen=screen
        self.asset=asset
        self.credit=1
        self.level=-1
        
        self.start_screen=True
        self.start_screen_sprite=StartScreen(self.screen,self.asset)
        self.playing_game=False
        
        self.levels=Level()
        self.launcher_sprite=Launcher(self.asset)
        
        self.font_type='all_font' # all_font, number, alphabet
    
    def set_start_screen_timer(self):
        if self.start_screen_sprite.count_time<=0:
            self.start_screen=False
            self.playing_game=True
    
    def next_level(self):
        self.level+=1
        bubble_size=16*SCALE
        for row,data in enumerate(self.levels.levels[f'level_{self.level+1}']['map']):
            for column,bubble in enumerate(data):
                if row%2==0:
                    x=column*bubble_size+STAGE_LEFT
                    y=row*bubble_size+STAGE_TOP-(bubble_size//8*row)
                elif row%2!=0:
                    x=column*bubble_size+(STAGE_LEFT+bubble_size//2)
                    y=row*bubble_size+STAGE_TOP-(bubble_size//8*row)
                
                row_index=row
                column_index=column
                
                if bubble!='_':
                    self.launcher_sprite.bubble_sprite.add(Bubble(self.asset,(x,y),bubble))
        
        self.launcher_sprite.load_bubble=Bubble(
            self.asset,(GRID_CELL_SIZE*19,GRID_CELL_SIZE*23),self.levels.levels[f'level_{self.level+1}']['start'][0],load=True)
        self.launcher_sprite.next_bubble=Bubble(
            self.asset,(GRID_CELL_SIZE*15,GRID_CELL_SIZE*25),self.levels.levels[f'level_{self.level+1}']['start'][1])
        self.launcher_sprite.bubble_sprite.add(self.launcher_sprite.load_bubble,self.launcher_sprite.next_bubble)
    
    def check_index(self):
        mouse_pos=pygame.mouse.get_pos()
        for bubble in self.launcher_sprite.bubble_sprite:
            if bubble.rect.collidepoint(mouse_pos):
                print(bubble)
    
    def draw_background(self):
        level=min(self.level//3,9)
        
        if self.level<24 or self.level>26:
            background=self.asset.background_images[level]
            background_rect=background.get_rect()
            floor=self.asset.floor_images[level]
            floor_rect=floor.get_rect(bottom=SCREEN_HEIGHT)
            self.screen.blits([[background,background_rect],[floor,floor_rect]])
        elif 23<self.level<27:
            special_background=self.asset.background_images[level]
            special_background_rect=special_background.get_rect()
            special_floor=self.asset.floor_images[level]
            special_floor_rect=special_floor.get_rect(bottom=SCREEN_HEIGHT)
            self.screen.blits([[special_background,special_background_rect],[special_floor,special_floor_rect]])
    
    def draw_text(self):
        bottom_text=list(f'`````````````````LEVEL-4`````CREDIT`{self.credit:0>2}``')
        for x,text in enumerate(bottom_text):
            if text!='`':
                self.font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][self.font_index]
                self.screen.blit(font,(x*GRID_CELL_SIZE,GRID_CELL_SIZE*27))
    
    def update(self):
        if self.start_screen:
            self.set_start_screen_timer()
        elif not self.start_screen and self.playing_game:
            self.launcher_sprite.update(self.level)
            self.check_index()
    
    def draw(self):
        if self.start_screen:
            self.start_screen_sprite.draw()
            self.draw_text()
        elif not self.start_screen and self.playing_game:
            self.draw_background()
            self.launcher_sprite.draw(self.screen)
            self.draw_text()
        # else:
        #     self.screen.fill('black')
        #     self.draw_text()