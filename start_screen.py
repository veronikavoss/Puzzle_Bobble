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
        
        self.font_type='all_font' # all_font, number, alphabet
        self.font_index=0
        self.count_time=30
        self.timer_update=pygame.time.get_ticks()
    
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
    
    def draw(self):
        self.screen.blit(self.background_image,self.background_rect)
        self.screen.blit(self.logo_image,self.logo_rect)
        self.screen.blit(self.taito_logo_image,self.taito_logo_rect)
        self.draw_text()