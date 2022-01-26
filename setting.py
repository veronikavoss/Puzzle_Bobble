from turtle import screensize
import pygame,os

TITLE='Puzzle Bobble'
SCALE=4
GRID_CELL_SIZE=8*SCALE
SCREEN_SIZE=SCREEN_WIDTH,SCREEN_HEIGHT=320*SCALE,224*SCALE # 1280,896
STAGE_SIZE=STAGE_WIDTH,STAGE_HEIGHT=128*SCALE,160*SCALE
STAGE_LEFT,STAGE_RIGHT,STAGE_TOP,STAGE_BOTTOM=GRID_CELL_SIZE*12,GRID_CELL_SIZE*20,GRID_CELL_SIZE*3,STAGE_HEIGHT
FPS=60

CURRENT_PATH=os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH=os.path.join(CURRENT_PATH,'image')