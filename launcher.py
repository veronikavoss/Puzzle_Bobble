from setting import *
from guide_point import GuidePoint
from bubble import Bubble
from borders import Border
from random import choice

class Launcher:
    def __init__(self,asset,level):
        self.asset=asset
        self.level=level
        self.game_status=None
        self.get_images()
        self.game_over=False
        
        self.speed=0
        self.angle=90
        self.guide_point_timer_update=0
        self.character1_update_time=pygame.time.get_ticks()
        self.character2_update_time=pygame.time.get_ticks()
        self.hurry_up_update_time=pygame.time.get_ticks()
        self.character1_animation_speed=0.1
        self.character2_animation_speed=0.1
        self.character_gravity=0
        self.launch_count=0
        
        self.guide_point_index=0
        self.guide_point_sprite=pygame.sprite.Group()
        self.load_bubble=pygame.sprite.GroupSingle()
        self.next_bubble=pygame.sprite.GroupSingle()
        self.bubble_cells=pygame.sprite.Group()
        self.bubble_sprite=pygame.sprite.Group()
        self.borders_sprite=pygame.sprite.GroupSingle(Border(self.asset,self.level))
    
    def set_character_images(self):
        self.character_1p_status={
            'character1_idle':self.asset.launcher_images['character'][0:1],
            'character1_delay1':[*self.asset.launcher_images['character'][0:2],*self.asset.launcher_images['character'][0:2]],
            'character1_delay2':[*self.asset.launcher_images['character'][1:3],*self.asset.launcher_images['character'][1:3]],
            'character1_blowing':self.asset.launcher_images['character'][3:9],
            'character1_load':self.asset.launcher_images['character'][6:9],
            'character1_hurry_up':self.asset.launcher_images['character'][9:11],
            'character1_clear':self.asset.launcher_images['character'][11:15],
            'character1_dead':self.asset.launcher_images['character'][15:23],
            'character2_idle':self.asset.launcher_images['character'][23:24],
            'character2_delay1':self.asset.launcher_images['character'][24:27],
            'character2_delay2':[*self.asset.launcher_images['character'][27:29],*self.asset.launcher_images['character'][27:29]],
            'character2_work':self.asset.launcher_images['character'][29:37],
            'character2_clear':self.asset.launcher_images['character'][37:41],
            'character2_dead':self.asset.launcher_images['character'][41:43],
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
        self.pointer_image=pygame.transform.rotate(self.pointer_image,-90)
        self.clone_pointer_image=self.pointer_image
        self.pointer_rect=self.pointer_image.get_rect(bottomleft=(GRID_CELL_SIZE*16,SCREEN_HEIGHT))
        self.pointer_rect_center=self.pointer_rect.center
        self.pointer_image_rect=self.pointer_image.get_rect(center=self.pointer_rect_center)
        
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
        self.character2_x=-3
        self.character2_image_flip=False
        
        self.character_2p_frame_index=0
        self.character_2p_image=self.character_2p_status['character_join'][self.character_2p_frame_index]
        self.character_2p_image_rect=self.character2_image.get_rect(bottomleft=(GRID_CELL_SIZE*32,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.bubbles_pocket_image1=self.asset.launcher_images['bubbles_pocket'][0]
        self.bubbles_pocket_image2=self.asset.launcher_images['bubbles_pocket'][1]
        self.bubbles_pocket_image_rect=self.bubbles_pocket_image1.get_rect(bottomleft=(GRID_CELL_SIZE*10,SCREEN_HEIGHT-GRID_CELL_SIZE))
        
        self.background_level=min((self.level+1)//3,10)
        self.borders_side_image=self.asset.borders_side_image[self.background_level]
        self.borders_side_image_rect=self.borders_side_image.get_rect(topleft=(GRID_CELL_SIZE*10,GRID_CELL_SIZE*2))
        
        self.hurry_up_images=self.asset.launcher_images['hurry_up']
        self.hurry_up_countdown_frame_index=0
        self.hurry_up_countdown_image=self.hurry_up_images[self.hurry_up_countdown_frame_index]
        self.hurry_up_countdown_image_rect=self.hurry_up_countdown_image.get_rect(bottomleft=(GRID_CELL_SIZE*11.5,SCREEN_HEIGHT-GRID_CELL_SIZE*2))
    
    def guide_point_cooldown(self):
        self.guide_point_timer_update=pygame.time.get_ticks()
        self.guide_point_index+=1
        if self.guide_point_index>=8:
            self.guide_point_index=0
    
    def set_guide_point(self):
        if self.current_time-self.guide_point_timer_update>=60:
            self.guide_point=GuidePoint(self.asset,self.guide_point_index)
            self.guide_point.set_angle(self.angle)
            self.guide_point_sprite.add(self.guide_point)
            self.guide_point_cooldown()
    
    def guide_point_collision(self):
        collide_bubble=pygame.sprite.groupcollide(self.guide_point_sprite,self.bubble_sprite,True,False,pygame.sprite.collide_mask)
        collide_ceiling=pygame.sprite.spritecollide(self.borders_sprite.sprite,self.guide_point_sprite,True,pygame.sprite.collide_mask)
    
    def set_key_input(self):
        key_input=pygame.key.get_pressed()
        if (self.game_status=='ready' or self.game_status=='playing') and not self.character1_status=='character1_clear':
            if key_input[pygame.K_LEFT] and self.angle<=175:
                self.speed=1.5
            elif key_input[pygame.K_RIGHT] and self.angle>=5:
                self.speed=-1.5
            else:
                self.speed=0
            if key_input[pygame.K_SPACE]:
                self.launch_bubble()
        
        self.angle+=self.speed
    
    def launch_bubble(self):
        if self.game_status=='playing' and \
        not self.load_bubble.sprite.launched and \
        self.load_bubble.sprite.load and \
        not self.character1_status=='character1_blowing':
            self.character1_status='character1_blowing'
            self.asset.launch_sound.play()
            self.character1_animation_speed=0.15
            self.pipe=True
            self.load_bubble.sprite.set_angle(self.angle)
            self.load_bubble.sprite.launched=True
            self.next_bubble.sprite.reload=True
            self.hurry_up_countdown_frame_index=0
    
    def set_launch_count(self):
        self.launch_count+=1
        if self.launch_count>6:
            self.borders_sprite.sprite.ceiling_down+=1
            self.move_the_bubbles_down()
            self.launch_count=0
    
    def move_the_bubbles_down(self):
        for bubble in self.bubble_sprite:
            bubble.set_rect((bubble.rect.x,bubble.rect.y+(14*SCALE)))
        for cell in self.bubble_cells:
            cell.set_rect((cell.rect.x,cell.rect.y+(14*SCALE)))
    
    def choice_bubble_color(self):
        bubble=choice(self.bubble_sprite.sprites())
        return bubble.color
    
    def create_bubble(self):
        if self.bubble_sprite:
            self.next_bubble.add(Bubble(self.asset,(GRID_CELL_SIZE*12,GRID_CELL_SIZE*25),self.choice_bubble_color(),create=True))
    
    def character1_delay_timer(self):
        self.character1_update_time=pygame.time.get_ticks()
    
    def character1_delay_animation(self):
        if (self.current_time-self.character1_update_time)//100==30:
            self.character1_status=choice(['character1_delay1','character1_delay2'])
        elif (self.current_time-self.hurry_up_update_time)//100==50:
            self.character1_status=self.hurry_up_timer()
    
    def hurry_up_timer(self):
        self.hurry_up_update_time=pygame.time.get_ticks()
        return 'character1_hurry_up'
    
    def character2_delay_timer(self):
        self.character2_update_time=pygame.time.get_ticks()
        return choice(['character2_delay1','character2_delay2'])
    
    def character2_delay_animation(self):
        if (self.current_time-self.character2_update_time)//100>=30:
            self.character2_status=self.character2_delay_timer()
    
    def set_idle_status(self):
        if not self.character1_status=='character1_blowing':
            if not self.character1_status=='character1_delay1' or not self.character1_status=='character1_delay2':
                if self.character1_status=='character1_idle':
                    self.character1_animation_speed=0.1
                    self.character1_delay_animation()
        
        if self.speed!=0:
            self.character2_status='character2_work'
            self.character2_delay_timer()
        else:
            if self.character2_status=='character2_delay1' or \
                self.character2_status=='character2_delay2' or \
                self.character2_status=='character2_dead' or \
                    self.character2_status=='character2_clear':
                self.character2_animation_speed=0.1
            else:
                self.character2_status='character2_idle'
                self.character2_delay_animation()
    
    def animation(self):
        # set_images
        angle_adjuster_animation=self.asset.launcher_images['angle_adjuster']
        controller_animation=self.asset.launcher_images['controller']
        pipe_animation=self.asset.launcher_images['pipe']
        character1_1p_animation=self.character_1p_status[self.character1_status]
        hurry_up_animation=self.hurry_up_images
        character2_1p_animation=self.character_1p_status[self.character2_status]
        character_2p_animation=self.character_2p_status['character_join']
        
        # set_frame_index_speed
        self.angle_adjuster_frame_index+=self.speed*0.5
        if self.angle_adjuster_frame_index>=len(angle_adjuster_animation) or self.angle_adjuster_frame_index<=-len(angle_adjuster_animation):
            self.angle_adjuster_frame_index=0
        
        self.controller_frame_index+=self.speed*0.5
        if self.controller_frame_index>=len(controller_animation) or self.controller_frame_index<=-len(controller_animation):
            self.controller_frame_index=0
        
        if self.pipe:
            self.pipe_frame_index+=0.2
        if self.pipe_frame_index>=len(pipe_animation):
            self.pipe_frame_index=0
            self.pipe=False
        
        # 1p character1
        self.character1_frame_index+=self.character1_animation_speed
        if self.character1_frame_index>=len(character1_1p_animation):
            self.character1_frame_index=0
            if self.character1_status=='character1_blowing':
                self.character1_delay_timer()
                self.hurry_up_timer()
                self.character1_status='character1_idle'
            elif self.character1_status=='character1_delay1' or self.character1_status=='character1_delay2':
                self.character1_status='character1_idle'
            elif self.character1_status=='character1_dead':
                self.character1_animation_speed=0.1
                self.character1_frame_index=4
        if self.character1_status=='character1_hurry_up':
            self.hurry_up_countdown_frame_index=(self.current_time-self.hurry_up_update_time)//500
            if self.hurry_up_countdown_frame_index>=len(hurry_up_animation):
                self.hurry_up_countdown_frame_index=0
                self.launch_bubble()
        
        if self.character1_status=='character1_clear':
            self.character1_animation_speed=0.2
            self.character_gravity+=0.2
            self.character1_image_rect.move_ip(0,self.character_gravity)
            if self.character1_image_rect.bottom>=SCREEN_HEIGHT-GRID_CELL_SIZE:
                self.character1_image_rect.bottom=SCREEN_HEIGHT-GRID_CELL_SIZE
                self.character_gravity=-4
            if self.character_gravity<0:
                if self.character1_frame_index>=2:
                    self.character1_frame_index=0
            elif self.character_gravity>0 and self.character1_frame_index<2:
                self.character1_frame_index=2
                if self.character1_frame_index>=4:
                    self.character1_frame_index=0
        
        # 1p character2
        self.character2_frame_index+=self.character2_animation_speed
        if self.character2_status=='character2_work':
            self.character2_frame_index=self.controller_frame_index
        if self.character2_frame_index>=len(character2_1p_animation) or self.character2_frame_index<=-len(character2_1p_animation):
            self.character2_frame_index=0
            if self.character2_status=='character2_delay1' or self.character2_status=='character2_delay2':
                self.character2_status='character2_idle'
                self.character2_delay_animation()
        
        if self.character2_status=='character2_clear':
            self.character2_animation_speed=0.1
            self.character2_image_rect.move_ip(self.character2_x,0)
            if self.character2_image_rect.left<=GRID_CELL_SIZE*21:
                self.character2_x=3
                self.character2_image_flip=True
            elif self.character2_image_rect.right>=GRID_CELL_SIZE*27:
                self.character2_x=-3
                self.character2_image_flip=False
        
        # 2p blue character
        self.character_2p_frame_index+=0.1
        if self.character_2p_frame_index>=len(character_2p_animation):
            self.character_2p_frame_index=0
        
        # set_images
        self.angle_adjuster_image=angle_adjuster_animation[int(self.angle_adjuster_frame_index)]
        self.controller_image=controller_animation[int(self.controller_frame_index)]
        self.pointer_image=pygame.transform.rotate(self.clone_pointer_image,self.angle)
        self.pointer_image_rect=self.pointer_image.get_rect(center=self.pointer_rect_center)
        self.pipe_image=pipe_animation[int(self.pipe_frame_index)]
        self.character1_image=character1_1p_animation[int(self.character1_frame_index)]
        self.hurry_up_countdown_image=hurry_up_animation[int(self.hurry_up_countdown_frame_index)]
        self.character2_image=character2_1p_animation[int(self.character2_frame_index)]
        self.character2_image=pygame.transform.flip(self.character2_image,self.character2_image_flip,False)
        self.character_2p_image=character_2p_animation[int(self.character_2p_frame_index)]
        self.borders_side_image=self.asset.borders_side_image[self.background_level]
    
    def update(self,level):
        self.current_time=pygame.time.get_ticks()
        if level==0:
            self.set_guide_point()
            self.guide_point_collision()
            self.guide_point_sprite.update()
        self.set_key_input()
        self.set_idle_status()
        self.animation()
        self.bubble_sprite.update()
        self.borders_sprite.update()
    
    def draw(self,screen):
        screen.blits([
            [self.boundary_image,self.boundary_image_rect],
            [self.angle_adjuster_image,self.angle_adjuster_image_rect],
            [self.controller_image,self.controller_image_rect],
            [self.pointer_image,self.pointer_image_rect],
            [self.pipe_image,self.pipe_image_rect],
            [self.bubbles_pocket_image1,self.bubbles_pocket_image_rect],
            [self.character1_image,self.character1_image_rect],
            [self.character2_image,self.character2_image_rect],
            [self.character_2p_image,self.character_2p_image_rect]
            ])
        
        self.guide_point_sprite.draw(screen)
        for bubble in self.bubble_sprite.sprites():
            bubble.draw_bubble(screen,self.launch_count)
        self.borders_sprite.sprite.draw(screen)
        if self.load_bubble.sprite:
            self.load_bubble.draw(screen)
        if self.next_bubble:
            self.next_bubble.draw(screen)
        
        screen.blits([
            [self.borders_side_image,self.borders_side_image_rect],
            [self.bubbles_pocket_image2,self.bubbles_pocket_image_rect]
            ])
        
        if self.character1_status=='character1_hurry_up':
            screen.blit(self.hurry_up_countdown_image,self.hurry_up_countdown_image_rect)
        # print(self.asset.launch_sound)