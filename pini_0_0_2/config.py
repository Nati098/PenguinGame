screen_width = 1366
screen_height = 768
background_image = "imgs/background.png"

HAND_PICS = {0:"imgs/hand.png", 1:"imgs/hand-fish.png", 2:"imgs/hand-boot.png", 3:"imgs/hand-ball.png"}
OBJECT_PICS = {0:"imgs/matras.png", 1:"imgs/vyshka.png", 2:"imgs/peschera.png", 3:"imgs/ryba.png", \
               4:"imgs/shariki.png", 5:"imgs/invent.png"}
SCALE_PICS = {0:"imgs/scale-hunger.png", 1:"imgs/scale-energy.png", \
              2:"imgs/scale-fun.png", 3:"imgs/scale-hand.png"}
scale_height = 50
PENG_PICS = "imgs/pen.png"

frame_rate = 90

font_name = 'Times New Roman'
font_size = 20

button_text_color = (255, 255, 255)
button_normal_back_color = (75, 0, 130)
button_hover_back_color = (75, 0, 130)
button_pressed_back_color = (75, 0, 130)

from enum import Enum
class StackAction(Enum):
    UPDATE_HAND_0 = 0
    UPDATE_HAND_1 = 1
    UPDATE_HAND_2 = 2
    UPDATE_HAND_3 = 3
    INTERACT_FISH = 4
    INTERACT_CAVE = 5
    INTERACT_MATTRESS = 6
    INTERACT_TOWER = 7
    INTERACT_BALLS = 8
    WALK_UP = 9
    WALK_DOWN = 10
    WALK_LEFT = 11
    WALK_RIGHT = 12
    WALK_UPLEFT = 13
    WALK_UPRIGHT = 14
    WALK_DOWNLEFT = 15
    WALK_DOWNRIGHT = 16
    INTERACT_HAND_1 = 17
    INTERACT_HAND_2 = 18
    INTERACT_HAND_3 = 19
