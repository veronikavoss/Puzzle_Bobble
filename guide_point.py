from setting import *
import math

class GuidePoint(pygame.sprite.Sprite):
    def __init__(self,asset,index):
        super().__init__()
        self.asset=asset
        self.image_index=index
        
        self.image=self.asset.guide_point_images[self.image_index]
        self.rect=self.image.get_rect(center=BUBBLE_LOAD_POS)
        
        self.radius=20
    
    def set_angle(self,angle):
        self.angle=angle
        self.rad_angle=math.radians(angle)
    
    def set_position(self):
        x=self.radius*math.cos(self.rad_angle)
        y=self.radius*math.sin(self.rad_angle)
        
        self.rect.x+=x
        self.rect.y-=y
        
        if self.rect.centerx<=STAGE_LEFT+BUBBLE_WIDTH//2:
            self.rect.left=STAGE_LEFT+BUBBLE_WIDTH//2
            self.set_angle(180-self.angle)
        elif  self.rect.centerx>=STAGE_RIGHT-BUBBLE_WIDTH//2:
            self.rect.right=STAGE_RIGHT-BUBBLE_WIDTH//2
            self.set_angle(180-self.angle)
    
    def update(self):
        self.set_position()