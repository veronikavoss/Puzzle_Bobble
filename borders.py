from setting import *

class Border(pygame.sprite.Sprite):
    def __init__(self,asset):
        super().__init__()
        self.asset=asset
        
        self.set_image()
        self.image=self.ceiling_image['level_1'][0]
        self.rect=self.image.get_rect(topleft=(GRID_CELL_SIZE*12,GRID_CELL_SIZE*2))
    
    def set_image(self):
        image=self.asset.borders_ceiling_image
        self.ceiling_image={
            'level_1':image[:12],
            'level_2':image[12:24],
            'level_3':image[24:36],
            'level_4':image[36:48],
            'level_5':image[48:60],
            'level_6':image[60:72],
            'level_7':image[72:84],
            'level_8':image[84:96],
            'level_9':image[96:108],
            'level_10':image[108:120]
            }