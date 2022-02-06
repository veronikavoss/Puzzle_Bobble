from setting import *

class StartScreen:
    def __init__(self,screen,asset):
        self.screen=screen
        self.asset=asset
        
        self.background_image=self.asset.start_screen_background
        self.background_rect=self.background_image.get_rect()
        
        self.logo_image=self.asset.logo
        self.logo_rect=self.logo_image.get_rect(midtop=(SCREEN_WIDTH//2,GRID_CELL_SIZE))
        
        self.taito_logo_image=self.asset.taito_logo
        self.taito_logo_rect=self.taito_logo_image.get_rect(midtop=(SCREEN_WIDTH//2,SCREEN_HEIGHT-GRID_CELL_SIZE*8))
        
        self.get_character_image()
        
        self.font_type='all_font' # all_font, number, alphabet
        self.font_index=0
        self.count_time=30
        self.timer_update=pygame.time.get_ticks()
    
    def get_character_image(self):
        self.character_images=self.asset.start_screen_characters
        
        self.character1_wink_image=[
            pygame.transform.flip(self.character_images['green'][0],True,False),
            *self.character_images['green'][16:19]
            ]
        self.character2_jump_image=[self.character_images['blue'][0],*self.character_images['blue'][13:15]]
        print(self.character1_wink_image)
        print(self.character2_jump_image)
        self.character1_frame_index=0
        self.character2_frame_index=0
        
        self.character1_image=self.character1_wink_image[self.character1_frame_index]
        # self.character1_image=pygame.transform.flip(self.character1_image,True,False)
        self.character1_image_rect=self.character1_image.get_rect(topleft=(GRID_CELL_SIZE*3,GRID_CELL_SIZE*17))
        
        self.character2_image=self.character2_jump_image[self.character2_frame_index]
        self.character2_image_rect=self.character2_image.get_rect(topright=(SCREEN_WIDTH-GRID_CELL_SIZE*3,GRID_CELL_SIZE*17))
    
    def animation(self):
        character1_animation=self.character1_wink_image
        character2_animation=self.character2_jump_image
        
        self.character1_frame_index+=0.05
        self.character2_frame_index+=0.05
        
        if self.character1_frame_index>=len(character1_animation):
            self.character1_frame_index=0
        
        if self.character2_frame_index>=len(character2_animation):
            self.character2_frame_index=0
        
        self.character1_image=character1_animation[int(self.character1_frame_index)]
        self.character2_image=character2_animation[int(self.character2_frame_index)]
    
    def draw_text(self):
        current_time=pygame.time.get_ticks()
        self.count_time=30-((current_time-self.timer_update)//1000)
        
        push_text=list('``````````PUSH`1P`SPACEBAR`KEY``````````')
        time_text=[
            list('``````````````````TIME``````````````````'),
            list(f'```````````````````{self.count_time:0>2}```````````````````')]
        
        for x,text in enumerate(push_text):
            if text!='`':
                self.font_index=ord(text)-33
                font=self.asset.font_images[self.font_type][self.font_index]
                if (current_time//600)%2==0:
                    self.screen.blit(font,(x*GRID_CELL_SIZE,GRID_CELL_SIZE*19))
        
        for row,text_data in enumerate(time_text):
            for column,text in enumerate(text_data):
                x=column*GRID_CELL_SIZE
                y=row*GRID_CELL_SIZE
                if text!='`':
                    self.font_index=ord(text)-33
                    font=self.asset.font_images[self.font_type][self.font_index]
                    self.screen.blit(font,(x,y+(GRID_CELL_SIZE*24)))
    
    def update(self):
        self.animation()
    
    def draw(self):
        self.screen.blits([
            [self.background_image,self.background_rect],
            [self.logo_image,self.logo_rect],
            [self.taito_logo_image,self.taito_logo_rect],
            [self.character1_image,self.character1_image_rect],
            [self.character2_image,self.character2_image_rect]
            ])
        self.draw_text()