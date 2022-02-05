from setting import *
from start_screen import StartScreen
from level import *
from launcher import Launcher
from bubble import Bubble, BubbleCell
from random import choice

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
        self.bubble_cell=pygame.sprite.Group()
        self.launcher_sprite=Launcher(self.asset)
        
        self.font_type='all_font' # all_font, number, alphabet
    
    def set_start_screen_timer(self):
        if self.start_screen_sprite.count_time<=0:
            self.start_screen=False
            self.playing_game=True
    
    def next_level(self):
        self.level+=1
        
        for row,data in enumerate(self.levels.levels[f'level_{self.level+1}']):
            for column,bubble in enumerate(data):
                self.bubble_cell.add(BubbleCell(self.set_bubble_position(row,column),(row,column)))
                if bubble!='_':
                    self.launcher_sprite.bubble_sprite.add(Bubble(self.asset,self.set_bubble_position(row,column),bubble,index=(row,column)))
        
        self.launcher_sprite.load_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*19,GRID_CELL_SIZE*23),self.launcher_sprite.choice_bubble_color()))
        
        self.launcher_sprite.next_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*15,GRID_CELL_SIZE*25),self.launcher_sprite.choice_bubble_color()))
    
    def set_bubble_position(self,row,column):
        if row%2==0:
            x=column*BUBBLE_WIDTH+STAGE_LEFT
            y=row*BUBBLE_HEIGHT+STAGE_TOP-(BUBBLE_HEIGHT//8*row)
        elif row%2!=0:
            x=column*BUBBLE_WIDTH+(STAGE_LEFT+BUBBLE_WIDTH//2)
            y=row*BUBBLE_HEIGHT+STAGE_TOP-(BUBBLE_HEIGHT//8*row)
        
        return x,y
    
    def get_map_index(self):
        for cell in self.bubble_cell:
            if cell.rect.collidepoint(self.launcher_sprite.load_bubble.sprite.rect.center):
                column_index=cell.index[0]
                row_index=cell.index[1]
                return column_index,row_index
    
    def bubbles_collision(self):
        load_bubble=self.launcher_sprite.load_bubble.sprite
        
        collide_bubble=pygame.sprite.spritecollideany(load_bubble,self.launcher_sprite.bubble_sprite,pygame.sprite.collide_mask)
        if collide_bubble:
            row_index,column_index=self.get_map_index()
            self.levels.levels[f'level_{self.level+2}'][row_index][column_index]=load_bubble.color
            self.launcher_sprite.load_bubble.sprite.set_rect(self.set_bubble_position(row_index,column_index))
            self.launcher_sprite.load_bubble.sprite.index=(row_index,column_index)
            self.launcher_sprite.bubble_sprite.add(self.launcher_sprite.load_bubble.sprite)
            self.launcher_sprite.load_bubble.sprite.launched=False
            self.launcher_sprite.load_bubble.add(self.launcher_sprite.next_bubble)
            self.launcher_sprite.create_bubble()
            # self.launcher_sprite.next_bubble.sprite.reload=True
        # print(load_bubble.rect,load_bubble.load,load_bubble.index)
        
        if pygame.sprite.collide_mask(load_bubble,self.launcher_sprite.borders_sprite.sprite):
            if load_bubble.rect.top<=self.launcher_sprite.borders_sprite.sprite.rect.bottom:
                self.launcher_sprite.load_bubble.sprite.add(self.launcher_sprite.next_bubble)
                self.launcher_sprite.create_bubble()
    
    def check_index(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.launcher_sprite.load_bubble.sprite.rect.collidepoint(mouse_pos):
            print(self.launcher_sprite.load_bubble.sprite.load,self.launcher_sprite.load_bubble.sprite.launched)
        for bubble in self.launcher_sprite.bubble_sprite:
            for cell in self.bubble_cell:
                if bubble.rect.collidepoint(mouse_pos):
                    print(bubble.rect,bubble.color,bubble.load,bubble.index)
                # if cell.rect.collidepoint(mouse_pos):
                #     print(cell.index)
    
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
            if self.launcher_sprite.load_bubble.sprite:
                self.launcher_sprite.load_bubble.sprite.update()
            self.launcher_sprite.next_bubble.update()
            self.launcher_sprite.update(self.level)
            self.bubbles_collision()
            self.check_index()
    
    def draw(self):
        if self.start_screen:
            self.start_screen_sprite.draw()
            self.draw_text()
        elif not self.start_screen and self.playing_game:
            self.draw_background()
            self.bubble_cell.draw(self.screen)
            self.launcher_sprite.draw(self.screen)
            self.draw_text()
        # else:
        #     self.screen.fill('black')
        #     self.draw_text()