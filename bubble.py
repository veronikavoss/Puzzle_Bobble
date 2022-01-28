from setting import *
from random import choice

class Bubble(pygame.sprite.Sprite):
    def __init__(self,asset,pos,color,load=False):
        super().__init__()
        self.asset=asset
        self.color=color
        self.load=load
        
        self.ready=False
        self.bubble_status='delay'
        self.bubble_frame_index=0
        self.set_bubbles_image()
        self.image=self.bubbles_status[self.bubble_status][self.bubble_frame_index]
        self.rect=self.image.get_rect(topleft=pos)
    
    def red_bubble(self,color):
        if self.bubble_status=='delay':
            if color=='R':
                bubble=self.asset.bubbles_image['R'][1:2]
            else:
                bubble=self.asset.bubbles_image[color][1:4]
            return bubble
        elif self.bubble_status=='dead':
            if color=='R':
                bubble=self.bubbles_dead_image['R'][1:2]
            else:
                bubble=self.bubbles_dead_image[color][1:4]
            return bubble
    
    def set_bubbles_image(self):
        self.bubbles_dead_image={
            'B':self.asset.bubbles_dead_image[:10],
            'Y':self.asset.bubbles_dead_image[11:21],
            'R':self.asset.bubbles_dead_image[22:32],
            'G':self.asset.bubbles_dead_image[33:43],
            'P':self.asset.bubbles_dead_image[44:54],
            'O':self.asset.bubbles_dead_image[55:65],
            'L':self.asset.bubbles_dead_image[66:76],
            'S':self.asset.bubbles_dead_image[77:87]}
        
        bubble_color=self.color
        # bubble_color='R'
        self.bubbles_status={
            'idle':self.asset.bubbles_image[bubble_color][1:2],
            'delay':self.red_bubble(bubble_color),
            'collide':self.asset.bubbles_image[bubble_color][5:],
            'pop':self.asset.bubbles_pop_image[bubble_color],
            'popped':self.asset.bubbles_popped_image[bubble_color][:4],
            'dead':self.red_bubble(bubble_color)
        }
    
    def animation(self):
        bubble_animation=self.bubbles_status[self.bubble_status]
        self.bubble_frame_index+=0.1
        if self.bubble_frame_index>=len(bubble_animation):
            self.bubble_frame_index=0
        self.image=bubble_animation[int(self.bubble_frame_index)]
    
    def move(self):
        self.rect.y-=3
    
    def set_ready(self):
        if self.ready:
            pass
    
    def update(self):
        self.animation()
        self.set_ready()