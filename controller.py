from setting import *
from start_screen import StartScreen
from level import *
from launcher import Launcher
from bubble import Bubble, BubbleCell, BubblePop
from random import choice

class Controller:
    def __init__(self,screen,asset):
        self.screen=screen
        self.asset=asset
        self.credit=1
        self.level=-1
        
        self.start_screen=True
        self.start_screen_sprite=StartScreen(self.screen,self.asset)
        
        self.level_data=Level()
        self.bubble_cell=pygame.sprite.Group()
        self.bubble_popped=pygame.sprite.Group()
        
        self.playing_game=False
        self.round_start=False
        self.round_update_time=0
        self.visited=[]
        
        self.font_type='all_font' # all_font, number, alphabet
    
    def set_start_screen_timer(self):
        if self.start_screen_sprite.count_time<=0:
            self.start_screen=False
            self.playing_game=True
            self.next_level()
    
    def next_level(self):
        self.launcher_sprite=Launcher(self.asset)
        self.level+=1
        
        self.round_start=True
        self.start_round_timer()
        
        for row,data in enumerate(self.level_data.levels[f'level_{self.level+1}']):
            for column,bubble in enumerate(data):
                self.bubble_cell.add(BubbleCell(self.set_bubble_position(row,column),(row,column)))
                if bubble!='_':
                    self.launcher_sprite.bubble_sprite.add(Bubble(self.asset,self.set_bubble_position(row,column),bubble,index=(row,column)))
        
        self.launcher_sprite.load_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*19,GRID_CELL_SIZE*23),self.launcher_sprite.choice_bubble_color()))
        
        self.launcher_sprite.next_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*15,GRID_CELL_SIZE*25),self.launcher_sprite.choice_bubble_color()))
    
    def start_round_timer(self):
        self.round_update_time=pygame.time.get_ticks()
    
    def popup_round_board(self):
        if self.round_start:
            if (self.current_time-self.round_update_time)//100<20:
                # round_board_image
                self.round_board_image=self.asset.round_board
                self.round_board_image_rect=self.round_board_image.get_rect(topleft=(GRID_CELL_SIZE*12,GRID_CELL_SIZE*6))
                self.screen.blit(self.round_board_image,self.round_board_image_rect)
                
                # round_board_text_image
                round_text=[list('ROUND'),list(f'{self.level+1:0>2}')]
                for column,text in enumerate(round_text[0]):
                    x=column*(16*SCALE)+GRID_CELL_SIZE*15
                    y=GRID_CELL_SIZE*7
                    font_index=ord(text)-55
                    font=self.asset.green_font_images['all_font'][font_index]
                    self.screen.blit(font,(x,y))
                
                for column,text in enumerate(round_text[1]):
                    x=column*(16*SCALE)+GRID_CELL_SIZE*18
                    y=GRID_CELL_SIZE*9
                    font_index=ord(text)-48
                    font=self.asset.green_font_images['all_font'][font_index]
                    self.screen.blit(font,(x,y))
    
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
    
    def visit(self,row_index,column_index,color):
        if row_index<0 or row_index>=STAGE_ROW or column_index<0 or column_index>=STAGE_COLUMN:
            return
        
        if self.level_data.levels[f'level_{self.level+1}'][row_index][column_index]!=color:
            return
        
        if (row_index,column_index) in self.visited:
            return
        
        self.visited.append((row_index,column_index))
        
        row=[0,-1,-1,0,1,1]
        column=[-1,-1,0,1,0,-1]
        if row_index%2==1:
            row=[0,-1,-1,0,1,1]
            column=[-1,0,1,1,1,0]
        
        for i in range(len(row)):
            self.visit(row_index+row[i],column_index+column[i],color)
    
    def remove_bubbles(self,row_index,column_index,color):
        self.visited.clear()
        self.visit(row_index,column_index,color)
        if len(self.visited)>=3:
            self.remove_visited_bubbles()
    
    def remove_visited_bubbles(self):
        for bubble in self.launcher_sprite.bubble_sprite.sprites():
            if bubble.index in self.visited:
                bubble.bubble_status='pop'
                self.launcher_sprite.load_bubble.sprite.bubble_status='pop'
                self.bubble_popped.add(BubblePop(self.asset,bubble.rect.center,bubble.color))
                bubble.set_rect((bubble.rect.x-(bubble.rect.w//2),(bubble.rect.y-(bubble.rect.h//2))))
                self.level_data.levels[f'level_{self.level+1}'][bubble.index[0]][bubble.index[1]]='_'
    
    def bubbles_collision(self):
        load_bubble=self.launcher_sprite.load_bubble.sprite
        
        bubble_n_bubble_collide=pygame.sprite.spritecollideany(load_bubble,self.launcher_sprite.bubble_sprite,pygame.sprite.collide_mask)
        ceiling_collide_bubble=pygame.sprite.spritecollideany(load_bubble,self.launcher_sprite.borders_sprite,pygame.sprite.collide_mask)
        
        if (bubble_n_bubble_collide and bubble_n_bubble_collide.bubble_status!='popped') or ceiling_collide_bubble:
                row_index,column_index=self.get_map_index()
                self.level_data.levels[f'level_{self.level+1}'][row_index][column_index]=load_bubble.color
                self.launcher_sprite.load_bubble.sprite.set_rect(self.set_bubble_position(row_index,column_index))
                self.launcher_sprite.load_bubble.sprite.bubble_status='collide'
                self.launcher_sprite.load_bubble.sprite.index=(row_index,column_index)
                self.launcher_sprite.bubble_sprite.add(self.launcher_sprite.load_bubble.sprite)
                self.remove_bubbles(row_index,column_index,load_bubble.color)
                self.launcher_sprite.load_bubble.sprite.launched=False
                self.launcher_sprite.load_bubble.add(self.launcher_sprite.next_bubble)
                self.launcher_sprite.create_bubble()
        
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
                font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][font_index]
                self.screen.blit(font,(x*GRID_CELL_SIZE,GRID_CELL_SIZE*27))
    
    def update(self):
        self.current_time=pygame.time.get_ticks()
        if self.start_screen:
            self.start_screen_sprite.update()
            self.set_start_screen_timer()
        elif not self.start_screen and self.playing_game:
            self.launcher_sprite.update(self.level)
            if self.launcher_sprite.load_bubble.sprite:
                self.launcher_sprite.load_bubble.sprite.update()
            self.launcher_sprite.next_bubble.update()
            self.bubbles_collision()
            self.bubble_popped.update()
            self.check_index()
    
    def draw(self):
        if self.start_screen:
            self.start_screen_sprite.draw()
            self.draw_text()
        elif not self.start_screen and self.playing_game:
            self.draw_background()
            self.bubble_cell.draw(self.screen)
            self.launcher_sprite.draw(self.screen)
            self.bubble_popped.draw(self.screen)
            self.draw_text()
            self.popup_round_board()
        # else:
        #     self.screen.fill('black')
        #     self.draw_text()