from itertools import count
from setting import *
from random import choice
import math

class Bubble(pygame.sprite.Sprite):
    def __init__(self,asset,pos,color,load=False,create=False,index=None):
        super().__init__()
        self.asset=asset
        self.color=color
        self.load=load
        self.create=create
        self.index=index
        
        self.delay_time=choice([3000,4000,5000])
        self.update_time=pygame.time.get_ticks()
        self.delay_animation_count=0
        
        self.launched=False
        self.reload=False
        self.bubble_status='idle'
        self.bubble_frame_index=0
        self.set_bubbles_image()
        self.image=self.bubbles_status[self.bubble_status][self.bubble_frame_index]
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.radius=18
    
    def red_bubble(self,color):
        if self.bubble_status=='idle':
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
            'normal':self.asset.bubbles_image[bubble_color][0:1],
            'idle':self.red_bubble(bubble_color),
            'collide':[self.asset.bubbles_image[bubble_color][1],*self.asset.bubbles_image[bubble_color][5:]],
            'pop':self.asset.bubbles_pop_image[bubble_color],
            'popped':self.asset.bubbles_popped_image[bubble_color][:4],
            'dead':self.red_bubble(bubble_color)
        }
    
    def delay_animation_timer(self):
        self.update_time=pygame.time.get_ticks()
    
    def delay_animation(self,bubble_animation):
        if self.color=='Y':
            self.bubble_frame_index+=0.5
            if self.bubble_frame_index>=len(bubble_animation):
                self.delay_animation_count+=1
                self.bubble_frame_index=0
                if self.delay_animation_count>=3:
                    self.delay_animation_count=0
                    self.delay_animation_timer()
        elif self.color=='B':
            self.bubble_frame_index+=0.1
            if self.bubble_frame_index>=len(bubble_animation):
                self.delay_animation_count+=1
                self.bubble_frame_index=0
                if self.delay_animation_count>=2:
                    self.delay_animation_count=0
                    self.delay_animation_timer()
        elif self.color=='L':
            self.bubble_frame_index+=0.2
            if self.bubble_frame_index>=len(bubble_animation):
                self.delay_animation_count+=1
                self.bubble_frame_index=0
                if self.delay_animation_count>=2:
                    self.delay_animation_count=0
                    self.delay_animation_timer()
        elif self.color=='O':
            self.bubble_frame_index+=0.5
            if self.bubble_frame_index>=len(bubble_animation):
                self.delay_animation_count+=1
                self.bubble_frame_index=0
                if self.delay_animation_count>=1:
                    self.delay_animation_count=0
                    self.delay_animation_timer()
        else:
            self.bubble_frame_index+=0.1
            if self.bubble_frame_index>=len(bubble_animation):
                self.bubble_frame_index=0
                self.delay_animation_timer()
    
    def animation(self):
        current_time=pygame.time.get_ticks()
        
        bubble_animation=self.bubbles_status[self.bubble_status]
        
        if self.bubble_status=='idle':
            if current_time-self.update_time>=self.delay_time:
                self.delay_animation(bubble_animation)
        elif self.bubble_status=='collide':
            self.bubble_frame_index+=0.3
            if self.bubble_frame_index>=len(bubble_animation):
                self.bubble_frame_index=0
                self.bubble_status='idle'
        elif self.bubble_status=='pop':
            self.bubble_frame_index+=0.3
            if self.bubble_frame_index>=len(bubble_animation):
                self.bubble_frame_index=0
                self.bubble_status='popped'
        elif self.bubble_status=='popped':
            self.bubble_frame_index+=0.1
            if self.bubble_frame_index>=len(bubble_animation):
                self.bubble_frame_index=0
                self.kill()
        else:
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
            self.direction.x=8
            if self.rect.x>=GRID_CELL_SIZE*15:
                self.direction.x=0
                self.rect.x=GRID_CELL_SIZE*15
                self.create=False
    
    def set_rect(self,topleft):
        self.rect=self.image.get_rect(topleft=topleft)
    
    def update(self):
        self.animation()
        self.launch()
        self.loading()

class BubbleCell(pygame.sprite.Sprite):
    def __init__(self,topleft,index):
        super().__init__()
        self.index=index
        self.image=pygame.Surface((BUBBLE_SIZE),pygame.SRCALPHA)
        self.image.fill((255,255,255,0))
        self.rect=self.image.get_rect(topleft=topleft)