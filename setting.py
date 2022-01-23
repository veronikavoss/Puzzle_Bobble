from turtle import screensize
import pygame,os

title='Puzzle Bobble'
scale=4
screen_size=screen_width,screen_height=320*scale,224*scale # 1280,896
stage_size=stage_width,stage_height=130*scale,200*scale # 520,800
grid_size=32
FPS=60

current_path=os.path.dirname(os.path.abspath(__file__))
image_path=os.path.join(current_path,'image')