from setting import *

class Asset:
    def __init__(self):
        self.general_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'General Sprites.png')).convert_alpha()
        self.background_1p_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'1Player Backgrounds.png')).convert_alpha()
        self.background_2p_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'2Player Backgrounds.png')).convert_alpha()
        self.borders_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'Borders.png')).convert_alpha()
        
        self.get_font_image()
        self.get_start_screen_image()
        self.get_background_image()
        self.get_launcher_image()
        self.get_balloon_image()
    
    def get_font_image(self):
        self.font_images={'all_font':[],'number':[],'alphabet':[]}
        
        for y in range(4):
            for x in range(31):
                surface=pygame.Surface((8,8))
                surface.blit(self.general_sheet,(0,0),(9*x+1,9*y+2195,8,8))
                surface=pygame.transform.scale(surface,(8*SCALE,8*SCALE))
                surface.set_colorkey((147,187,236))
                self.font_images['all_font'].append(surface)
        
        # 0,31,62,93
        del self.font_images['all_font'][111:] # 110
        self.font_images['all_font'].insert(62,self.font_images['all_font'][90])
        self.font_images['number']=self.font_images['all_font'][15:25] # 10
        self.font_images['alphabet']=self.font_images['all_font'][32:58] # 26
    
    def get_start_screen_image(self):
        self.start_screen_background=pygame.Surface((320,224))
        self.start_screen_background.blit(self.general_sheet,(0,0),(1,10,320,224))
        self.start_screen_background=pygame.transform.scale(self.start_screen_background,(320*SCALE,224*SCALE))
        self.start_screen_background.set_colorkey((147,187,236))
        
        self.logo=pygame.Surface((192,144))
        self.logo.blit(self.general_sheet,(0,0),(595,462,192,144))
        self.logo=pygame.transform.scale(self.logo,(192*SCALE,144*SCALE))
        self.logo.set_colorkey((147,187,236))
        
        self.taito_logo=pygame.Surface((112,32))
        self.taito_logo.blit(self.general_sheet,(0,0),(17,3126,112,32))
        self.taito_logo=pygame.transform.scale(self.taito_logo,(112*SCALE,32*SCALE))
        self.taito_logo.set_colorkey((147,187,236))
    
    def get_background_image(self):
        self.background_images=[]
        self.floor_images=[]
        
        for y in range(3):
            for x in range(3):
                surface=pygame.Surface((320,224))
                surface.blit(self.background_1p_sheet,(0,0),(328*x+16,264*y+16,320,224))
                surface=pygame.transform.scale(surface,(320*SCALE,224*SCALE))
                # surface.set_colorkey((180,253,194))
                self.background_images.append(surface)
        
        special=pygame.Surface((320,672))
        special.blit(self.background_1p_sheet,(0,0),(1000,16,320,672))
        special=pygame.transform.scale(special,(320*SCALE,672*SCALE))
        self.background_images.insert(8,special)
        
        for y in range(3):
            for x in range(3):
                surface=pygame.Surface((320,8))
                surface.blit(self.background_1p_sheet,(0,0),(328*x+16,264*y+248,320,8))
                surface=pygame.transform.scale(surface,(320*SCALE,8*SCALE))
                surface.set_colorkey((180,253,194))
                self.floor_images.append(surface)
        
        special_floor=pygame.Surface((320,8))
        special_floor.blit(self.background_1p_sheet,(0,0),(1000,696,320,8))
        special_floor=pygame.transform.scale(special_floor,(320*SCALE,8*SCALE))
        special_floor.set_colorkey((180,253,194))
        self.floor_images.insert(8,special_floor)
    
    def get_launcher_image(self):
        self.launcher_images={'pointer':[],'angle_adjuster':[],'balloons_pocket':[],'controller':[],'pipe':[],'character':[]}
        # 2p - balloons_pocket = [2:]3, character = [57:]113
                
        for y in range(4):
            for x in range(16):
                surface=pygame.Surface((64,64))
                surface.blit(self.general_sheet,(0,0),(65*x+1,65*y+1545,64,64))
                surface=pygame.transform.scale(surface,(64*SCALE,64*SCALE))
                surface.set_colorkey((147,187,236))
                self.launcher_images['pointer'].append(surface)
        
        for x in range(12):
            surface=pygame.Surface((64,40))
            surface.blit(self.general_sheet,(0,0),(65*x+1,1805,64,40))
            surface=pygame.transform.scale(surface,(64*SCALE,40*SCALE))
            surface.set_colorkey((147,187,236))
            self.launcher_images['angle_adjuster'].append(surface)
        
        for x in range(4):
            surface=pygame.Surface((64,32))
            surface.blit(self.general_sheet,(0,0),(65*x+781,1813,64,32))
            surface=pygame.transform.scale(surface,(64*SCALE,32*SCALE))
            surface.set_colorkey((147,187,236))
            self.launcher_images['balloons_pocket'].append(surface)
        
        for y in range(2):
            for x in range(4):
                surface=pygame.Surface((16,16))
                surface.blit(self.general_sheet,(0,0),(17*x+1041,17*y+1812,16,16))
                surface=pygame.transform.scale(surface,(16*SCALE,16*SCALE))
                surface.set_colorkey((147,187,236))
                self.launcher_images['controller'].append(surface)
        
        for x in range(4):
            surface=pygame.Surface((16,32))
            surface.blit(self.general_sheet,(0,0),(17*x+1041,1779,16,32))
            surface=pygame.transform.scale(surface,(16*SCALE,32*SCALE))
            surface.set_colorkey((147,187,236))
            self.launcher_images['pipe'].append(surface)
        
        for y in range(4):
            for x in range(29):
                surface=pygame.Surface((32,32))
                surface.blit(self.general_sheet,(0,0),(33*x+1,33*y+2012,32,32))
                surface=pygame.transform.scale(surface,(32*SCALE,32*SCALE))
                surface.set_colorkey((147,187,236))
                self.launcher_images['character'].append(surface)
        del self.launcher_images['character'][57]
        del self.launcher_images['character'][114]
    
    def get_balloon_image(self):
        self.balloons_image={'blue':[],'yellow':[],'red':[],'green':[],'purple':[],'orange':[],'black':[],'gray':[]}
        count=0
        for y,color in enumerate(self.balloons_image.keys()):
            y=(count//2)
            for x in range(10):
                surface=pygame.Surface((16,16))
                if count%2==0:
                    surface.blit(self.general_sheet,(0,0),(17*x+1,33*y+1854,16,16))
                else:
                    surface.blit(self.general_sheet,(0,0),(17*x+555,33*y+1854,16,16))
                surface=pygame.transform.scale(surface,(16*SCALE,16*SCALE))
                surface.set_colorkey((147,187,236))
                self.balloons_image[color].append(surface)
            count+=1
    
    # 320,224
    # 320 672 1000 16