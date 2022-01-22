from turtle import screensize
import pygame,os

title='Puzzle Bobble'
scale=3
screen_size=screen_width,screen_height=320,224
stage_size=stage_width,stage_height=130,200
FPS=60

current_path=os.path.dirname(os.path.abspath(__file__))
image_path=os.path.join(current_path,'image')