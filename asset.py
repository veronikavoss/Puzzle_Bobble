from setting import *

class Asset:
    def __init__(self):
        self.general_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'General Sprites.png')).convert_alpha()
        self.background_1p_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'1Player Backgrounds.png')).convert_alpha()
        self.background_2p_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'2Player Backgrounds.png')).convert_alpha()
        self.borders_sheet=pygame.image.load(os.path.join(IMAGE_PATH,'Borders_fix.png')).convert_alpha()
        
        self.get_font_n_ui_image()
        self.get_start_screen_image()
        self.get_background_n_Borders_image()
        self.get_launcher_image()
        self.get_bubble_image()
    
    def get_font_n_ui_image(self):
        # font_images
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
        
        # round_board_image
        self.round_board=pygame.Surface((128,48))
        self.round_board.blit(self.general_sheet,(0,0),(290,2178,128,48))
        self.round_board=pygame.transform.scale(self.round_board,(128*SCALE,48*SCALE))
        self.round_board.set_colorkey((147,187,236))
    
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
        
        self.start_screen_characters={'green':[],'blue':[]}
        for y,color in enumerate(self.start_screen_characters.keys()):
            for x in range(21):
                surface=pygame.Surface((48,48))
                surface.blit(self.general_sheet,(0,0),(49*x+1,49*y+364,48,48))
                surface=pygame.transform.scale(surface,(48*SCALE,48*SCALE))
                surface.set_colorkey((147,187,236))
                self.start_screen_characters[color].append(surface)
    
    def get_background_n_Borders_image(self):
        # background image
        self.background_images=[]
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
        
        # floor image
        self.floor_images=[]
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
        
        # boundary image
        self.boundary_image=pygame.Surface((128,16))
        self.boundary_image.blit(self.general_sheet,(0,0),(581,2185,128,16))
        self.boundary_image=pygame.transform.scale(self.boundary_image,(128*SCALE,16*SCALE))
        self.boundary_image.set_colorkey((147,187,236))
        
        # borders image
        self.borders_side_image=[]
        for y in range(10):
            surface=pygame.Surface((160,200))
            surface.blit(self.borders_sheet,(0,0),(1,250*y+10,160,200))
            surface=pygame.transform.scale(surface,(160*SCALE,200*SCALE))
            # surface.set_colorkey((147,187,236))
            surface.set_colorkey((50,97,168))
            self.borders_side_image.append(surface)
        
        self.borders_ceiling_image=[]
        for y in range(10):
            for count in range(2):
                for x in range(6):
                    if count==0:
                        surface=pygame.Surface((128,78))
                        surface.blit(self.borders_sheet,(0,0),(129*x+162,250*y+10,128,78))
                        surface=pygame.transform.scale(surface,(128*SCALE,78*SCALE))
                        # surface.set_colorkey((147,187,236))
                        surface.set_colorkey((50,97,168))
                        self.borders_ceiling_image.append(surface)
                    else:
                        surface=pygame.Surface((128,162))
                        surface.blit(self.borders_sheet,(0,0),(129*x+162,250*y+91,128,162))
                        surface=pygame.transform.scale(surface,(128*SCALE,162*SCALE))
                        # surface.set_colorkey((147,187,236))
                        surface.set_colorkey((50,97,168))
                        self.borders_ceiling_image.append(surface)
    
    def get_launcher_image(self):
        # guide_point_images
        self.guide_point_images=[]
        for y in range(2):
            for x in range(4):
                surface=pygame.Surface((8,8))
                surface.blit(self.general_sheet,(0,0),(9*x+1041,9*y+1761,8,8))
                surface=pygame.transform.scale(surface,(8*SCALE,8*SCALE))
                surface.set_colorkey((147,187,236))
                self.guide_point_images.append(surface)
        
        # launcher_images
        self.launcher_images={'pointer':[],'angle_adjuster':[],'bubbles_pocket':[],'controller':[],'pipe':[],'character':[]}
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
            self.launcher_images['bubbles_pocket'].append(surface)
        
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
    
    def get_bubble_image(self):
        # B=BLUE L=BLACK S=SILVER
        self.bubbles_image={'B':[],'Y':[],'R':[],'G':[],'P':[],'O':[],'L':[],'S':[]}
        self.bubbles_pop_image={'B':[],'Y':[],'R':[],'G':[],'P':[],'O':[],'L':[],'S':[]}
        self.bubbles_popped_image={'B':[],'Y':[],'R':[],'G':[],'P':[],'O':[],'L':[],'S':[]}
        self.bubbles_dead_image=[]
        
        count=0
        for y,color in enumerate(self.bubbles_image.keys()):
            y=count//2
            for x in range(10):
                surface=pygame.Surface((16,16))
                if count%2==0:
                    surface.blit(self.general_sheet,(0,0),(17*x+1,33*y+1854,16,16))
                else:
                    surface.blit(self.general_sheet,(0,0),(17*x+555,33*y+1854,16,16))
                surface=pygame.transform.scale(surface,(16*SCALE,16*SCALE))
                surface.set_colorkey((147,187,236))
                self.bubbles_image[color].append(surface)
            count+=1
        
        count=0
        for y,color in enumerate(self.bubbles_image.keys()):
            y=count//2
            for x in range(7):
                surface=pygame.Surface((32,32))
                if count%2==0:
                    surface.blit(self.general_sheet,(0,0),(33*x+171,33*y+1846,32,32))
                else:
                    surface.blit(self.general_sheet,(0,0),(33*x+725,33*y+1846,32,32))
                surface=pygame.transform.scale(surface,(32*SCALE,32*SCALE))
                surface.set_colorkey((147,187,236))
                self.bubbles_pop_image[color].append(surface)
            count+=1
        
        count=0
        for y,color in enumerate(self.bubbles_image.keys()):
            y=count//2
            for x in range(9):
                surface=pygame.Surface((16,16))
                if count%2==0:
                    surface.blit(self.general_sheet,(0,0),(17*x+402,33*y+1854,16,16))
                else:
                    surface.blit(self.general_sheet,(0,0),(17*x+956,33*y+1854,16,16))
                surface=pygame.transform.scale(surface,(16*SCALE,16*SCALE))
                surface.set_colorkey((147,187,236))
                self.bubbles_popped_image[color].append(surface)
            count+=1
        
        for y in range(2):
            for x in range(11*4):
                surface=pygame.Surface((16,16))
                surface.blit(self.general_sheet,(0,0),(17*x+1,17*y+1978,16,16))
                surface=pygame.transform.scale(surface,(16*SCALE,16*SCALE))
                surface.set_colorkey((147,187,236))
                self.bubbles_dead_image.append(surface)
    
    # 320,224
    # 320 672 1000 16