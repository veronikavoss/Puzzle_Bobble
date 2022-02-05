from guide_point import GuidePoint
from setting import *
from bubble import Bubble
from borders import Border
from random import choice

class Launcher:
    def __init__(self,asset):
        self.asset=asset
        self.status='idle'
        self.get_images()
        
        self.speed=0
        self.angle=90
        self.update_time=0
        self.index=0
        
        self.load_bubble=pygame.sprite.GroupSingle()
        self.next_bubble=pygame.sprite.GroupSingle()
        
        self.guide_point_sprite=pygame.sprite.Group()
        self.bubble_sprite=pygame.sprite.Group()
        self.borders_sprite=pygame.sprite.GroupSingle(Border(self.asset))
    
    def set_character_images(self):
        self.character_1p_status={
            'character1_idle':self.asset.launcher_images['character'][0:1],
            'character1_delay1':self.asset.launcher_images['character'][0:2],
            'character1_delay2':self.asset.launcher_images['character'][1:3],
            'character1_load':self.asset.launcher_images['character'][6:9],
            'character1_blowing':self.asset.launcher_images['character'][3:6],
            'character1_hurry_up':self.asset.launcher_images['character'][9:11],
            'character1_clear':self.asset.launcher_images['character'][11:15],
            'character1_die':self.asset.launcher_images['character'][15:23],
            'character2_idle':self.asset.launcher_images['character'][23:24],
            'character2_delay1':self.asset.launcher_images['character'][24:27],
            'character2_delay2':self.asset.launcher_images['character'][27:29],
            'character2_work':self.asset.launcher_images['character'][29:37],
            'character2_clear':self.asset.launcher_images['character'][37:41],
            'character2_die':self.asset.launcher_images['character'][41:43],
            'character_join':self.asset.launcher_images['character'][43:53],
            'character_thankyou':self.asset.launcher_images['character'][53:57]}
        
        self.character_2p_status={
            'character_join':self.asset.launcher_images['character'][100:110],
            'character_thankyou':self.asset.launcher_images['character'][110:114]
            }
    
    def get_images(self):
        self.boundary_image=self.asset.boundary_image
        self.boundary_image_rect=self.boundary_image.get_rect(topleft=(GRID_CELL_SIZE*12,STAGE_BOTTOM))
        
        self.angle_adjuster_frame_index=0
        self.angle_adjuster_image=self.asset.launcher_images['angle_adjuster'][self.angle_adjuster_frame_index]
        self.angle_adjuster_image_rect=self.angle_adjuster_image.get_rect(bottomleft=(GRID_CELL_SIZE*16,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.controller_frame_index=0
        self.controller_image=self.asset.launcher_images['controller'][self.controller_frame_index]
        self.controller_image_rect=self.controller_image.get_rect(bottomleft=(GRID_CELL_SIZE*22,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.pointer_frame_index=0
        self.pointer_image=self.asset.launcher_images['pointer'][self.pointer_frame_index]
        self.pointer_rect=self.pointer_image.get_rect(bottomleft=(GRID_CELL_SIZE*16,SCREEN_HEIGHT))
        
        self.pipe=False
        self.pipe_frame_index=0
        self.pipe_image=self.asset.launcher_images['pipe'][self.pointer_frame_index]
        self.pipe_image_rect=self.pipe_image.get_rect(bottomleft=(GRID_CELL_SIZE*19,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.set_character_images()
        self.character1_status='character1_idle'
        self.character1_frame_index=0
        self.character1_image=self.character_1p_status[self.character1_status][self.character1_frame_index]
        self.character1_image_rect=self.character1_image.get_rect(bottomleft=(GRID_CELL_SIZE*16,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.character2_status='character2_idle'
        self.character2_frame_index=0
        self.character2_image=self.character_1p_status[self.character2_status][self.character2_frame_index]
        self.character2_image_rect=self.character2_image.get_rect(bottomleft=(GRID_CELL_SIZE*22,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.character_2p_frame_index=0
        self.character_2p_image=self.character_2p_status['character_join'][self.character_2p_frame_index]
        self.character_2p_image_rect=self.character2_image.get_rect(bottomleft=(GRID_CELL_SIZE*32,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.bubbles_pocket_image1=self.asset.launcher_images['bubbles_pocket'][0]
        self.bubbles_pocket_image2=self.asset.launcher_images['bubbles_pocket'][1]
        self.bubbles_pocket_image_rect=self.bubbles_pocket_image1.get_rect(bottomleft=(GRID_CELL_SIZE*10,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        # self.borders_ceiling_image=self.asset.borders_ceiling_image[0]
        # self.borders_ceiling_image_rect=self.borders_ceiling_image.get_rect(topleft=(GRID_CELL_SIZE*12,GRID_CELL_SIZE*2))
        
        self.borders_side_image=self.asset.borders_side_image[0]
        self.borders_side_image_rect=self.borders_side_image.get_rect(topleft=(GRID_CELL_SIZE*10,GRID_CELL_SIZE*2))
    
    def guide_point_cooldown(self):
        self.update_time=pygame.time.get_ticks()
        self.index+=1
        if self.index>=8:
            self.index=0
    
    def set_guide_point(self):
        current_time=pygame.time.get_ticks()
        if current_time-self.update_time>=60:
            self.guide_point=GuidePoint(self.asset,self.index)
            self.guide_point.set_angle(self.angle)
            self.guide_point_sprite.add(self.guide_point)
            self.guide_point_cooldown()
    
    def set_key_input(self):
        key_input=pygame.key.get_pressed()
        if key_input[pygame.K_LEFT] and self.pointer_frame_index>=-len(self.asset.launcher_images['pointer'])+5:
            self.speed=-1
        elif key_input[pygame.K_RIGHT] and self.pointer_frame_index<=len(self.asset.launcher_images['pointer'])-5:
            self.speed=1
        else:
            self.speed=0
        if key_input[pygame.K_SPACE]:
            self.launch_bubble()
        
        self.angle+=self.speed*-1.45
    
    def launch_bubble(self):
        if not self.load_bubble.sprite.launched and self.load_bubble.sprite.load:
            self.character1_status='character1_blowing'
            self.pipe=True
            self.load_bubble.sprite.set_angle(self.angle)
            self.load_bubble.sprite.launched=True
            self.loading_bubble()
            
    
    def loading_bubble(self):
        self.next_bubble.sprite.reload=True
    
    def choice_bubble_color(self):
        bubble=choice(self.bubble_sprite.sprites())
        return bubble.color
    
    def create_bubble(self):
        self.next_bubble.add(Bubble(self.asset,(GRID_CELL_SIZE*12,GRID_CELL_SIZE*25),self.choice_bubble_color(),create=True))
    
    def set_status(self):
        if self.speed!=0:
            self.character2_status='character2_work'
        else:
            self.character2_status='character2_idle'
    
    def guide_point_collision(self):
        for point in self.guide_point_sprite:
            if pygame.sprite.collide_mask(point,self.borders_sprite.sprite):
                point.kill()
            for bubble in self.bubble_sprite:
                if pygame.sprite.collide_rect(point,bubble):
                    if not bubble.load:
                        point.kill()
    
    def animation(self):
        # set_images
        angle_adjuster_animation=self.asset.launcher_images['angle_adjuster']
        controller_animation=self.asset.launcher_images['controller']
        pointer_animation=self.asset.launcher_images['pointer']
        pipe_animation=self.asset.launcher_images['pipe']
        character1_1p_animation=self.character_1p_status[self.character1_status]
        character2_1p_animation=self.character_1p_status[self.character2_status]
        character_2p_animation=self.character_2p_status['character_join']
        
        # set_frame_index
        self.angle_adjuster_frame_index+=self.speed*0.5
        self.controller_frame_index+=self.speed*0.5
        self.pointer_frame_index+=self.speed
        flip_pointer_frame_index=self.pointer_frame_index*-1
        if self.pipe:
            self.pipe_frame_index+=0.2
        self.character1_frame_index+=0.2
        if self.character2_status=='character2_work':
            self.character2_frame_index=self.controller_frame_index
        else:
            self.character2_frame_index+=0.1
        self.character_2p_frame_index+=0.1
        
        if self.angle_adjuster_frame_index>=len(angle_adjuster_animation) or self.angle_adjuster_frame_index<=-len(angle_adjuster_animation):
            self.angle_adjuster_frame_index=0
        
        if self.controller_frame_index>=len(controller_animation) or self.controller_frame_index<=-len(controller_animation):
            self.controller_frame_index=0
        
        if self.pointer_frame_index>=len(pointer_animation) or self.pointer_frame_index<=-len(pointer_animation):
            self.pointer_frame_index=0
            
        if self.character1_frame_index>=len(character1_1p_animation):
            self.character1_frame_index=0
            if self.character1_status=='character1_blowing':
                # self.loading_bubble()
                self.character1_status='character1_load'
            elif self.character1_status=='character1_load':
                self.character1_status='character1_idle'
            
        if self.pipe_frame_index>=len(pipe_animation):
            self.pipe_frame_index=0
            self.pipe=False
        
        if self.character2_frame_index>=len(character2_1p_animation) or self.character2_frame_index<=-len(character2_1p_animation):
            self.character2_frame_index=0
        
        if self.character_2p_frame_index>=len(character_2p_animation):
            self.character_2p_frame_index=0
        
        # set_images
        self.angle_adjuster_image=angle_adjuster_animation[int(self.angle_adjuster_frame_index)]
        self.controller_image=controller_animation[int(self.controller_frame_index)]
        
        if self.pointer_frame_index<0:
            self.pointer_image=pointer_animation[int(flip_pointer_frame_index)]
            self.pointer_image=pygame.transform.flip(self.pointer_image,True,False)
        else:
            self.pointer_image=pointer_animation[int(self.pointer_frame_index)]
        
        self.pipe_image=pipe_animation[int(self.pipe_frame_index)]
        self.character1_image=character1_1p_animation[int(self.character1_frame_index)]
        self.character2_image=character2_1p_animation[int(self.character2_frame_index)]
        self.character_2p_image=character_2p_animation[int(self.character_2p_frame_index)]
    
    def update(self,level):
        if level==0:
            self.set_guide_point()
            self.guide_point_collision()
            self.guide_point_sprite.update()
        self.set_key_input()
        self.set_status()
        self.animation()
        self.bubble_sprite.update()
    
    def draw(self,screen):
        screen.blits([
            [self.boundary_image,self.boundary_image_rect],
            [self.angle_adjuster_image,self.angle_adjuster_image_rect],
            [self.controller_image,self.controller_image_rect],
            [self.pointer_image,self.pointer_rect],
            [self.pipe_image,self.pipe_image_rect],
            [self.bubbles_pocket_image1,self.bubbles_pocket_image_rect],
            [self.character1_image,self.character1_image_rect],
            [self.character2_image,self.character2_image_rect],
            [self.character_2p_image,self.character_2p_image_rect]
            ])
        self.guide_point_sprite.draw(screen)
        self.bubble_sprite.draw(screen)
        self.borders_sprite.draw(screen)
        if self.load_bubble.sprite:
            self.load_bubble.draw(screen)
        if self.next_bubble:
            self.next_bubble.draw(screen)
        screen.blits([
            [self.borders_side_image,self.borders_side_image_rect],
            [self.bubbles_pocket_image2,self.bubbles_pocket_image_rect]])
        
        # print(self.load_bubble.load,self.load_bubble)
        # print(self.collide_bubble)
        