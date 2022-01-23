from setting import *

class Asset:
    def __init__(self):
        self.general_sheet=pygame.image.load(os.path.join(image_path,'General Sprites.png')).convert_alpha()
        self.background_1p_sheet=pygame.image.load(os.path.join(image_path,'1Player Backgrounds.png')).convert_alpha()
        self.background_2p_sheet=pygame.image.load(os.path.join(image_path,'2Player Backgrounds.png')).convert_alpha()
        self.borders_sheet=pygame.image.load(os.path.join(image_path,'Borders.png')).convert_alpha()
        
        self.get_font_image()
        self.get_start_screen()
    
    def get_font_image(self):
        self.font_images={'all_font':[],'number':[],'alphabet':[]}
        
        for y in range(4):
            for x in range(31):
                surface=pygame.Surface((8,8))
                surface.blit(self.general_sheet,(0,0),(9*x+1,9*y+2195,8,8))
                surface=pygame.transform.scale(surface,(8*scale,8*scale))
                surface.set_colorkey((147,187,236))
                self.font_images['all_font'].append(surface)
        
        # 0,31,62,93
        del self.font_images['all_font'][111:] # 110
        self.font_images['all_font'].insert(62,self.font_images['all_font'][90])
        self.font_images['number']=self.font_images['all_font'][15:25] # 10
        self.font_images['alphabet']=self.font_images['all_font'][32:58] # 26
    
    def get_start_screen(self):
        self.start_screen_background=pygame.Surface((320,224))
        self.start_screen_background.blit(self.general_sheet,(0,0),(1,10,320,224))
        self.start_screen_background=pygame.transform.scale(self.start_screen_background,screen_size)
        self.start_screen_background.set_colorkey((147,187,236))
        
        self.logo=pygame.Surface((192,144))
        self.logo.blit(self.general_sheet,(0,0),(595,462,192,144))
        self.logo=pygame.transform.scale(self.logo,(192*scale,144*scale))
        self.logo.set_colorkey((147,187,236))
        
        self.taito_logo=pygame.Surface((112,32))
        self.taito_logo.blit(self.general_sheet,(0,0),(17,3126,112,32))
        self.taito_logo=pygame.transform.scale(self.taito_logo,(112*scale,32*scale))
        self.taito_logo.set_colorkey((147,187,236))
    
        # 112 32