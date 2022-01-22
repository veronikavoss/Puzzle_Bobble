from setting import *

class Asset:
    def __init__(self):
        self.general_sheet=pygame.image.load(os.path.join(image_path,'General Sprites.png')).convert_alpha()
        self.background_1p_sheet=pygame.image.load(os.path.join(image_path,'1Player Backgrounds.png')).convert_alpha()
        self.background_2p_sheet=pygame.image.load(os.path.join(image_path,'2Player Backgrounds.png')).convert_alpha()
        self.borders_sheet=pygame.image.load(os.path.join(image_path,'Borders.png')).convert_alpha()