from itertools import count
from setting import *
from random import choice
import math

class Bubble(pygame.sprite.Sprite):
    def __init__(self,asset,pos,color,load=False,create=False):
        super().__init__()
        self.asset=asset
        self.color=color
        self.load=load
        self.create=create
        
        self.launched=False
        self.reload=False
        self.bubble_status='delay'
        self.bubble_frame_index=0
        self.set_bubbles_image()
        self.image=self.bubbles_status[self.bubble_status][self.bubble_frame_index]
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.radius=18
    
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
    
    def set_angle(self,angle):
        self.angle=angle
        self.rad_angle=math.radians(angle)
    
    def launch(self):
        if self.launched:
            x=self.radius*math.cos(self.rad_angle)
            y=self.radius*math.sin(self.rad_angle)
            
            self.rect.x+=x
            self.rect.y-=y
            
            if self.rect.left<=STAGE_LEFT:
                self.rect.left=STAGE_LEFT
                self.set_angle(180-self.angle)
            elif  self.rect.right>=STAGE_RIGHT:
                self.rect.right=STAGE_RIGHT
                self.set_angle(180-self.angle)
    
    def loading(self):
        # reload
        if self.reload:
            self.rect.x+=self.direction.x
            self.rect.y+=self.direction.y
            self.direction.x=4
            self.direction.y=-2
            if self.rect.x>=GRID_CELL_SIZE*19:
                self.direction.x=0
                self.rect.x=GRID_CELL_SIZE*19
                # 480 608 128
            if self.rect.y<=GRID_CELL_SIZE*23:
                self.direction.y=0
                self.rect.y=GRID_CELL_SIZE*23
                # 800 736 -64
        if self.rect.x==GRID_CELL_SIZE*19 and self.rect.y==GRID_CELL_SIZE*23:
            self.reload=False
            self.load=True
        else:
            self.load=False
        
        # create
        if self.create and self.rect.x<=GRID_CELL_SIZE*15:
            self.rect.x+=self.direction.x
            self.rect.y+=self.direction.y
            self.direction.x=4
            if self.rect.x>=GRID_CELL_SIZE*15:
                self.direction.x=0
                self.rect.x=GRID_CELL_SIZE*15
                self.create=False
    
    def update(self):
        self.animation()
        self.launch()
        self.loading()
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)