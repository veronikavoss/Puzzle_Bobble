from setting import *
import math

class GuidePoint(pygame.sprite.Sprite):
    def __init__(self,asset,index,angle):
        super().__init__()
        self.asset=asset
        self.image_index=index
        
        self.image=self.asset.guide_point_images[self.image_index]
        self.rect=self.image.get_rect(center=BUBBLE_LOAD_POS)
        self.angle=angle
        
        # self.r=8*SCALE//2
        self.radius=18
    
    def set_angle(self):
        if self.rect.left<=STAGE_LEFT:
            self.rect.left=STAGE_LEFT
            self.rad_angle=math.radians(180-self.angle)
        elif  self.rect.right>=STAGE_RIGHT:
            self.rect.right=STAGE_RIGHT
            self.rad_angle=math.radians(180-self.angle)
        else:
            self.rad_angle=math.radians(self.angle)
    
    def set_position(self):
        x=self.radius*math.cos(self.rad_angle)
        y=self.radius*math.sin(self.rad_angle)
        
        self.rect.x+=x
        self.rect.y-=y
        
        # if self.rect.left<=STAGE_LEFT:
        #     x=self.radius*math.cos(self.rad_angle)*-1
        #     print(self.angle)
            # self.set_angle(180-self.angle)
        
    def update(self):
        self.set_angle()
        self.set_position()