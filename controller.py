from setting import *
from start_screen import StartScreen
from level import Level
from launcher import Launcher
from bubble import *

class Controller:
    def __init__(self,screen,asset):
        self.screen=screen
        self.asset=asset
        self.credit=1
        self.level=-1
        
        self.total_score=0
        self.drop_bubbles_score=0
        self.time_bonus_score=0
        
        self.start_screen=False
        self.start_screen_sprite=StartScreen(self.screen,self.asset)
        self.bubble_popped=pygame.sprite.Group()
        self.drop_bonus_score=pygame.sprite.GroupSingle()
        
        self.playing_game=False
        self.game_over=False
        self.play_time=0
        self.popup_round_board_timer_update=0
        self.game_over_timer_update=0
        self.game_over_countdown=0
        self.restart=False
        self.cell_index=pygame.sprite.GroupSingle()
        self.visited=[]
        
        self.ready_sound=False
        self.go_sound=False
        self.dead_sound_status=False
        self.clear_sound=False
        self.continue_sound=False
        self.game_over_sound=False
        
        self.font_type='all_font' # all_font, number, alphabet
    
    def set_start_screen_timer(self):
        if self.start_screen_sprite.count_time<=0:
            self.start_screen=False
            self.playing_game=True
            self.round_start()
    
    def round_start(self):
        self.level_data=Level()
        self.launcher_sprite=Launcher(self.asset,self.level)
        self.launcher_sprite.load_bubble.empty()
        self.launcher_sprite.next_bubble.empty()
        self.launcher_sprite.bubble_sprite.empty()
        self.level+=1
        
        self.ready_sound=False
        self.go_sound=False
        self.clear_sound=False
        self.dead_sound_status=False
        self.continue_sound=False
        self.game_over_sound=False
        self.launcher_sprite.game_status='ready'
        self.popup_round_board_timer()
        
        for row,data in enumerate(self.level_data.levels[f'level_{self.level+1}']):
            for column,bubble in enumerate(data):
                if bubble!='/':
                    self.launcher_sprite.bubble_cells.add(BubbleCell(self.set_bubble_position(row,column),(row,column)))
                if bubble!='_' and bubble!='/':
                    self.launcher_sprite.bubble_sprite.add(Bubble(self.asset,self.set_bubble_position(row,column),bubble,index=(row,column)))
        
        self.create_start_launch_bubble()
    
    def set_bubble_position(self,row,column):
        if row%2==0:
            x=column*BUBBLE_WIDTH+STAGE_LEFT
            y=row*BUBBLE_HEIGHT+STAGE_TOP+(self.launcher_sprite.borders_sprite.sprite.ceiling_down*(14*SCALE)-(BUBBLE_HEIGHT//8*row))
        elif row%2!=0:
            x=column*BUBBLE_WIDTH+(STAGE_LEFT+BUBBLE_WIDTH//2)
            y=row*BUBBLE_HEIGHT+STAGE_TOP+(self.launcher_sprite.borders_sprite.sprite.ceiling_down*(14*SCALE)-(BUBBLE_HEIGHT//8*row))
        
        return x,y
    
    def create_start_launch_bubble(self):
        self.launcher_sprite.load_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*19,GRID_CELL_SIZE*23),self.launcher_sprite.choice_bubble_color()))
        
        self.launcher_sprite.next_bubble.add(Bubble(
            self.asset,(GRID_CELL_SIZE*15,GRID_CELL_SIZE*25),self.launcher_sprite.choice_bubble_color()))
    
    def popup_round_board_timer(self):
        self.popup_round_board_timer_update=pygame.time.get_ticks()
    
    def game_timer(self):
        self.game_over_timer_update=pygame.time.get_ticks()
    
    def set_game_status(self):
        if not self.launcher_sprite.game_status=='dead' and not self.launcher_sprite.game_status=='clear':
            if (self.current_time-self.popup_round_board_timer_update)//100<20:
                self.launcher_sprite.game_status='ready'
            else:
                self.play_time=(self.current_time-self.game_over_timer_update)//1000
                self.launcher_sprite.game_status='playing'
    
    def popup_round_board(self):
        if self.launcher_sprite.game_status=='ready':
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
    
    def bubbles_collision(self):
        load_bubble=self.launcher_sprite.load_bubble.sprite
        
        bubble_n_bubble_collide=pygame.sprite.spritecollideany(load_bubble,self.launcher_sprite.bubble_sprite,pygame.sprite.collide_mask)
        ceiling_collide_bubble=pygame.sprite.spritecollideany(load_bubble,self.launcher_sprite.borders_sprite,pygame.sprite.collide_mask)
        if (bubble_n_bubble_collide and bubble_n_bubble_collide.bubble_status!='pop') or ceiling_collide_bubble:
            self.get_map_index()
            row_index,column_index=self.cell_index.sprite.index
            self.level_data.levels[f'level_{self.level+1}'][row_index][column_index]=load_bubble.color
            self.launcher_sprite.load_bubble.sprite.set_rect(self.set_bubble_position(row_index,column_index))
            self.launcher_sprite.load_bubble.sprite.bubble_status='collide'
            self.asset.collide_sound.play()
            self.launcher_sprite.load_bubble.sprite.index=(row_index,column_index)
            self.launcher_sprite.bubble_sprite.add(self.launcher_sprite.load_bubble.sprite)
            self.remove_bubbles(row_index,column_index,load_bubble.color)
            self.launcher_sprite.load_bubble.sprite.launched=False
            # self.check_game_over()
            self.launcher_sprite.load_bubble.add(self.launcher_sprite.next_bubble)
            self.launcher_sprite.set_launch_count()
            self.launcher_sprite.create_bubble()
        
        if pygame.sprite.collide_mask(load_bubble,self.launcher_sprite.borders_sprite.sprite):
            if load_bubble.rect.top<=self.launcher_sprite.borders_sprite.sprite.rect.bottom:
                self.launcher_sprite.load_bubble.sprite.add(self.launcher_sprite.next_bubble)
                self.launcher_sprite.create_bubble()
    
    def get_map_index(self):
        for cell in self.launcher_sprite.bubble_cells:
            if cell.rect.collidepoint(self.launcher_sprite.load_bubble.sprite.rect.center):
                self.cell_index.add(cell)
        if self.cell_index:
            return self.cell_index.sprite.index
    
    def visit(self,row_index,column_index,color=None):
        if row_index<0 or row_index>=STAGE_ROW or column_index<0 or column_index>=STAGE_COLUMN:
            return
        
        if color and self.level_data.levels[f'level_{self.level+1}'][row_index][column_index]!=color:
            return
        
        if self.level_data.levels[f'level_{self.level+1}'][row_index][column_index] in ['_','/']:
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
            self.remove_popped_bubbles()
            self.remove_dropped_bubbles()
            if not self.launcher_sprite.bubble_sprite:
                self.round_clear()
    
    def remove_popped_bubbles(self):
        for bubble in self.launcher_sprite.bubble_sprite:
            if bubble.index in self.visited:
                self.level_data.levels[f'level_{self.level+1}'][bubble.index[0]][bubble.index[1]]='_'
                self.bubble_popped.add(BubblePop(self.asset,bubble.rect.center,bubble.color))
                self.bubble_popped.add(BubblePopped(self.asset,bubble.rect.center,bubble.color))
                self.bubble_popped.add(BubblePopScore(self.asset,bubble.rect.center))
                self.total_score+=10
                self.launcher_sprite.bubble_sprite.remove(bubble)
                self.asset.collide_sound.stop()
                self.asset.pop_sound.play()
                self.asset.bubble_score_sound.play()
    
    def remove_dropped_bubbles(self):
        self.visited.clear()
        for column_index in range(STAGE_COLUMN):
            if self.level_data.levels[f'level_{self.level+1}'][0][column_index]!='_':
                self.visit(0,column_index)
        self.drop_bubbles()
    
    def drop_bubbles(self):
        drop_bubbles=[b for b in self.launcher_sprite.bubble_sprite if b.index not in self.visited]
        if drop_bubbles:
            for bubble in drop_bubbles:
                self.level_data.levels[f'level_{self.level+1}'][bubble.index[0]][bubble.index[1]]='_'
                self.launcher_sprite.bubble_sprite.remove(bubble)
                self.bubble_popped.add(BubbleDrop(self.asset,bubble.rect.center,bubble.color))
                self.bubble_popped.add(BubblePopScore(self.asset,bubble.rect.center))
                self.total_score+=10
            self.drop_bubbles_score=(2**len(drop_bubbles))*10
            self.drop_bonus_score.add(BubbleDropScore(self.asset,self.drop_bubbles_score))
            self.total_score+=self.drop_bubbles_score
    
    def round_clear(self):
        self.launcher_sprite.game_status='clear'
        self.launcher_sprite.character1_status='character1_clear'
        self.launcher_sprite.character2_status='character2_clear'
        self.popup_round_board_timer()
        self.set_time_bonus()
        self.launcher_sprite.bubble_sprite.empty()
        # if not self.launcher_sprite.load_bubble and self.launcher_sprite.next_bubble.sprite:
            # self.bubble_popped.add(BubblePop(self.asset,self.launcher_sprite.next_bubble.sprite.rect.center,self.launcher_sprite.next_bubble.sprite.color))
            # self.launcher_sprite.next_bubble.empty()
        # elif self.launcher_sprite.load_bubble:
            # self.bubble_popped.add(BubblePop(self.asset,self.launcher_sprite.load_bubble.sprite.rect.center,self.launcher_sprite.load_bubble.sprite.color))
            # self.launcher_sprite.load_bubble.empty()
        self.cell_index.empty()
    
    def set_time_bonus(self):
        if self.play_time<=5:
            self.time_bonus_score=50000
            self.total_score+=self.time_bonus_score
        elif self.play_time<=60:
            self.time_bonus_score=50000-(840*(self.play_time-5))
            self.total_score+=self.time_bonus_score
        else:
            self.time_bonus_score=0
    
    def next_round(self):
        #if self.launcher_sprite.character1_status=='character1_clear':
        if self.launcher_sprite.game_status=='clear':
            if (self.current_time-self.popup_round_board_timer_update)//100==40:
                self.asset.round_clear_sound.stop()
                self.round_start()
    
    def check_game_over(self):
        for bubble in self.launcher_sprite.bubble_sprite:
            if bubble.index and bubble.rect.centery>STAGE_BOTTOM:
                self.player_dead()
    
    def player_dead(self):
        self.launcher_sprite.game_over=True
        self.launcher_sprite.game_status='dead'
        self.launcher_sprite.character1_status='character1_dead'
        self.launcher_sprite.character2_status='character2_dead'
        if not self.dead_sound_status:
            pygame.mixer.music.stop()
            self.asset.dead_sound.play()
            self.asset.dead_voice_sound.play()
            self.dead_sound_status=True
        self.launcher_sprite.load_bubble.sprite.bubble_status='dead'
        self.launcher_sprite.load_bubble.sprite.set_bubbles_image()
        self.launcher_sprite.next_bubble.sprite.bubble_status='dead'
        self.launcher_sprite.next_bubble.sprite.set_bubbles_image()
        for bubble in self.launcher_sprite.bubble_sprite.sprites():
            bubble.bubble_status='dead'
            bubble.set_bubbles_image()
    
    def game_over_timer(self):
        if not self.game_over:
            self.game_over_timer_update=pygame.time.get_ticks()
            self.game_over=True
    
    def set_continue(self):
        if self.launcher_sprite.game_status=='dead':
            self.game_over_timer()
            if self.current_time-self.game_over_timer_update>=2000:
                self.playing_game=False
                self.game_over=False
                self.launcher_sprite.game_status='continue'
    
    def draw_continue(self):
        self.game_over_timer()
        self.game_over_countdown=10-((self.current_time-self.game_over_timer_update)//1000)
        continue_text=list('PUSH_START_BUTTON_TO_CONTINUE'),list(f'TIMER_{self.game_over_countdown:0>2}')
        for x,text in enumerate(continue_text[0]):
            if text!='_':
                font_index=ord(text)-33
                font_org=self.asset.font_images[self.font_type][font_index]
                font_copy=pygame.Surface.copy(font_org)
                pixelarray=pygame.PixelArray(font_copy)
                pixelarray.replace((248,248,248),(248,248,16))
                pixelarray.replace((136,136,136),(136,136,0))
                del pixelarray
                x=x*GRID_CELL_SIZE+(GRID_CELL_SIZE*5)
                y=GRID_CELL_SIZE*14
                self.screen.blit(font_copy,(x,y))
        for x,text in enumerate(continue_text[1]):
            if text!='_':
                font_index=ord(text)-33
                font_org=self.asset.font_images[self.font_type][font_index]
                font_copy=pygame.Surface.copy(font_org)
                pixelarray=pygame.PixelArray(font_copy)
                pixelarray.replace((248,248,248),(248,248,16))
                pixelarray.replace((136,136,136),(136,136,0))
                del pixelarray
                x=x*GRID_CELL_SIZE+(GRID_CELL_SIZE*16)
                y=GRID_CELL_SIZE*16
                self.screen.blit(font_copy,(x,y))
    
    def set_game_over(self):
        if self.game_over_countdown<0:
            self.launcher_sprite.game_status='game_over'
            self.game_over=False
            self.game_over_countdown=0
        if self.launcher_sprite.game_status=='game_over':
            self.game_over_timer()
            if self.current_time-self.game_over_timer_update>=7000:
                self.asset.game_over_sound.stop()
                self.restart=True
        
    def draw_game_over(self):
        game_over_text=list('GAME_OVER')
        for x,text in enumerate(game_over_text):
            if text!='_':
                font_index=ord(text)-55
                font=self.asset.green_font_images['all_font'][font_index]
                x=x*(16*SCALE)+(GRID_CELL_SIZE*11)
                y=GRID_CELL_SIZE*12
                self.screen.blit(font,(x,y))
    
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
    
    def draw_bottom_text(self):
        bottom_text=list(f'`````````````````LEVEL-4`````CREDIT`{self.credit:0>2}``')
        for x,text in enumerate(bottom_text):
            if text!='`':
                font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][font_index]
                self.screen.blit(font,(x*GRID_CELL_SIZE,GRID_CELL_SIZE*27))
    
    def draw_top_text(self):
        top_text=list('1UP'),list(f'{self.total_score:0>8}'),list('INSERT_COIN')
        
        for x,text in enumerate(top_text[0]):
            x=x*GRID_CELL_SIZE+(GRID_CELL_SIZE*3)
            font_index=ord(text)-33
            font_org=self.asset.font_images[self.font_type][font_index]
            font_copy=pygame.Surface.copy(font_org)
            pixelarray=pygame.PixelArray(font_copy)
            pixelarray.replace((248,248,248),(16,248,16))
            pixelarray.replace((136,136,136),(0,136,0))
            del pixelarray
            self.screen.blit(font_copy,(x,0))
        for x,text in enumerate(top_text[1]):
            x=x*GRID_CELL_SIZE+(GRID_CELL_SIZE*4)
            font_index=ord(text)-33
            font=self.asset.font_images[self.font_type][font_index]
            self.screen.blit(font,(x,GRID_CELL_SIZE))
        for x,text in enumerate(top_text[2]):
            if text!='_':
                x=SCREEN_WIDTH-(GRID_CELL_SIZE*(13-x))
                font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][font_index]
                if self.current_time//1000%2==0:
                    self.screen.blit(font,(x,GRID_CELL_SIZE))
    
    def draw_round_clear_text(self):
        if self.launcher_sprite.game_status=='clear':
            clear_round_text=list('ROUND_CLEAR'),list(f'{self.play_time:_>2}_SEC'),list(f'{self.time_bonus_score:_>5}_PTS'),list('NO_BONUS')
            # round clear
            if (self.current_time-self.popup_round_board_timer_update)//100<20:
                for column,text in enumerate(clear_round_text[0]):
                    if text!='_':
                        x=column*(16*SCALE)+GRID_CELL_SIZE*9
                        y=GRID_CELL_SIZE*10
                        font_index=ord(text)-55
                        font=self.asset.green_font_images['all_font'][font_index]
                        self.screen.blit(font,(x,y))
            else:
                # play time
                for column,text in enumerate(clear_round_text[1]):
                    if text!='_':
                        x=column*(16*SCALE)+GRID_CELL_SIZE*14
                        y=GRID_CELL_SIZE*8
                        font_index=ord(text)-48
                        if text=='S' or text=='E' or text=='C':
                            font_index=ord(text)-55
                        font=self.asset.green_font_images['all_font'][font_index]
                        self.screen.blit(font,(x,y))
                # time bonus
                # if self.game_timer_update<=5:
                if self.time_bonus_score!=0:
                    for column,text in enumerate(clear_round_text[2]):
                        if text!='_':
                            x=column*(16*SCALE)+GRID_CELL_SIZE*11
                            y=GRID_CELL_SIZE*12
                            font_index=ord(text)-48
                            if text=='P' or text=='T' or text=='S':
                                font_index=ord(text)-55
                            font=self.asset.green_font_images['all_font'][font_index]
                            self.screen.blit(font,(x,y))
                else:
                    for column,text in enumerate(clear_round_text[3]):
                        if text!='_':
                            x=column*(16*SCALE)+GRID_CELL_SIZE*12
                            y=GRID_CELL_SIZE*12
                            font_index=ord(text)-55
                            font=self.asset.green_font_images['all_font'][font_index]
                            self.screen.blit(font,(x,y))
    
    def play_sounds(self):
        if self.launcher_sprite.game_status=='ready' and not self.ready_sound:
            pygame.mixer.music.play(-1)
            self.asset.ready_sound.play()
            self.ready_sound=True
        elif self.launcher_sprite.game_status=='playing' and not self.go_sound:
            self.game_timer()
            self.asset.ready_sound.stop()
            self.asset.go_sound.play()
            self.go_sound=True
        elif self.launcher_sprite.game_status=='clear' and not self.clear_sound:
            pygame.mixer.music.stop()
            self.asset.pop_sound.stop()
            self.asset.round_clear_sound.play()
            self.clear_sound=True
        elif self.launcher_sprite.game_status=='continue' and not self.continue_sound:
            self.asset.round_clear_sound.stop()
            self.asset.continue_sound.play()
            self.continue_sound=True
        elif self.launcher_sprite.game_status=='game_over' and not self.game_over_sound:
            self.asset.continue_sound.stop()
            self.asset.game_over_sound.play()
            self.game_over_sound=True
    
    def check_index(self):
        mouse_pos=pygame.mouse.get_pos()
        if self.launcher_sprite.load_bubble.sprite.rect.collidepoint(mouse_pos):
            print(self.launcher_sprite.load_bubble.sprite.load,self.launcher_sprite.load_bubble.sprite.launched)
        for bubble in self.launcher_sprite.bubble_sprite:
            for cell in self.launcher_sprite.bubble_cells:
                if cell.rect.collidepoint(mouse_pos):
                    # print(bubble.rect,bubble.color,bubble.load,bubble.index)
                    print(cell.rect,cell.index)
        if pygame.sprite.groupcollide(self.launcher_sprite.bubble_cells,self.launcher_sprite.bubble_cells,False,False,pygame.sprite.collide_mask):
            print(1)
    
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
            self.set_game_status()
            self.next_round()
            self.check_game_over()
            self.play_sounds()
            self.check_index()
            self.drop_bonus_score.update()
            self.set_continue()
        elif not self.start_screen and not self.playing_game:
            self.set_game_over()
            self.play_sounds()
    
    def draw(self):
        if self.start_screen:
            self.start_screen_sprite.draw()
            self.draw_bottom_text()
        elif not self.start_screen and self.playing_game:
            self.draw_background()
            self.launcher_sprite.bubble_cells.draw(self.screen)
            self.launcher_sprite.draw(self.screen)
            self.bubble_popped.draw(self.screen)
            self.draw_bottom_text()
            self.draw_top_text()
            self.popup_round_board()
            self.draw_round_clear_text()
            if self.drop_bonus_score:
                self.drop_bonus_score.sprite.draw(self.screen)
        elif not self.start_screen and not self.playing_game:
            self.screen.fill((0,0,0))
            if self.launcher_sprite.game_status=='continue':
                self.draw_continue()
            elif self.launcher_sprite.game_status=='game_over':
                self.draw_game_over()