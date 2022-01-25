from setting import *
from random import choice

class Balloon(pygame.sprite.Sprite):
    def __init__(self,asset,pos):
        super().__init__()
        self.asset=asset
        
        self.set_balloons_image()
        self.balloon_status='idle'
        self.balloon_frame_index=0
        self.image=self.balloons_status[self.balloon_status][self.balloon_frame_index]
        self.rect=self.image.get_rect(bottomleft=pos)
    
    def red_balloon(self,color):
        if color=='red':
            balloon=self.asset.balloons_image['red'][1:2]
        else:
            balloon=self.asset.balloons_image[color][1:4]
        return balloon
    
    def set_balloons_image(self):
        balloon_color=choice(list(self.asset.balloons_image.keys()))
        self.balloons_status={
            'idle':self.asset.balloons_image[balloon_color][1:2],
            'delay':self.red_balloon(balloon_color),
            'collide':self.asset.balloons_image[balloon_color][5:11]
        }
    
    def animation(self):
        balloon_animation=self.balloons_status[self.balloon_status]
        self.balloon_frame_index+=0.1
        if self.balloon_frame_index>=len(balloon_animation):
            self.balloon_frame_index=0
        self.image=balloon_animation[int(self.balloon_frame_index)]
    
    def update(self):
        self.animation()