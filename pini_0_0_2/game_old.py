import pygame, sys, math, random, time
from pygame.constants import K_q, K_w, K_e, K_r
from ple.games import base
import numpy as np
from logger import *
from bica import *
#  logger args: actor, action, params, pen_state, hand_state

#remove when bica will be added
pen_state = [0,0]
hand_state = [0,0]

MOVE_OFFSET = 15
LEFT = 1
RIGHT = 3
INTERACT_DISTANCE = 200
size = width, height = 1366, 768
window = pygame.display.set_mode(size, pygame.RESIZABLE)
screen = pygame.Surface((1366,768))
coords = (0, 0, 0)
pygame.font.init()
BTN_FONT = pygame.font.SysFont('Calibri', 12)
TEXT_FONT = pygame.font.SysFont('Calibri', 32)
GAME_OVER = pygame.image.load("imgs/game_over.jpg")
RESULTS_FILE = "results.txt"

stack = []
stack_hand = []
objects = {"cave": 0, "matress": 0, "food": 0, "DULL": 0, "hill": 0, "balls": 0}


def increase(obj):
    objects[obj] += 1

def add_action(code):
    stack.append(code)

def change_score(score, add):
    '''for i in range(len(score)):
        if (0 <= (score[i]+add[i]) < 100):
            score[i] = score[i]+add[i]
        elif score[i]+add[i] < 0:
            score[i] = 0
        else:
            score[i] = 100'''
    for i in range(len(score)):
        score[i] = score[i] + add[i]
    return score

def optimal_path(paths):
    lenghts = [len(i) for i in paths]
    return paths[np.argmax(lenghts)]

class Console(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.message = "Meet Pinja, a little and cute penguin. He's your pet now!"
    def setMessage(self, msg):
        self.message = msg
    def render(self):
        self.msg_surface = TEXT_FONT.render(self.message, False, (255,255,255))
        window.blit(self.msg_surface, (320, 690))

console = Console()
class GameObject(pygame.sprite.Sprite):
    states = ['matress', 'hill', 'cave', 'food', 'balls']
    i_string = ""
    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)
        if state in self.states:
            self.state = state
            if state == 'matress':
                self.sprite = pygame.image.load("imgs/matras.png")
                self.x, self.y = 70, 440
                self.i_string = "Pinja laid on a matress"
                self.reward = [0,+5,+5,0]
            if state == 'hill':
                self.sprite = pygame.image.load("imgs/vyshka.png")
                self.x, self.y = 650, 300
                self.i_string = "Pinja jumped down from a hill"
                self.reward = [0,-3,+10,0]
            if state == 'cave':
                self.sprite = pygame.image.load("imgs/peschera.png")
                self.x, self.y = 85, 130
                self.i_string = "Pinja slept in a cave"
                self.reward = [+3,+10,0,0]
            if state == 'food':
                self.sprite = pygame.image.load("imgs/ryba.png")
                self.x, self.y = 1185, 277
                self.i_string = "Pinja ate some fish"
                self.reward = [+10,+3,+3,0]
            if state == 'balls':
                self.sprite = pygame.image.load("imgs/shariki.png")
                self.x, self.y = 1175, 640
                self.i_string = "Pinja played with balls"
                self.reward = [-3,-7,+10,0]
            '''if state == 'DULL':
                self.sprite = None
                self.x, self.y = 0,0
                self.i_string = ""
                self.reward = [0,0,0,0]'''
            self.width, self.height = self.sprite.get_size()

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
    def render(self):
        if self.sprite is not None:
            screen.blit(self.sprite, (self.x, self.y))
    def interact(self, console, score, bica, logger, command=False):
        #print(score, self.reward)
        score = change_score(score, self.reward)
        increase(self.state)
        #print(self.i_string)
        bica.interact(self.state, command)
        logger.add("penguin",self.state,score)
        console.setMessage(self.i_string)
        return score


class Button(pygame.sprite.Sprite):
    states = ['TICKLE', 'CARESS', 'THREATEN', 'COMMAND', 'GAME_OVER']

    i_string = ''
    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)

        if state in self.states:
            self.state = state
            if state == 'TICKLE':
                self.x, self.y = 185, 0
                self.bounds = pygame.Rect(self.x, self.y, 120, 60)
                self.i_string = "Tickle"
            if state == 'CARESS':
                self.x, self.y = 310, 0
                self.bounds = pygame.Rect(self.x, self.y, 120, 60)
                self.i_string = "Pat"
            if state == 'THREATEN':
                self.x, self.y = 435, 0
                self.bounds = pygame.Rect(self.x, self.y, 120, 60)
                self.i_string = "Threaten"
            if state == 'COMMAND':
                self.x, self.y = 560, 0
                self.bounds = pygame.Rect(self.x, self.y, 120, 60)
                self.i_string = "Command"
            if state == 'GAME_OVER':
                self.x, self.y = 1245, 0
                self.bounds = pygame.Rect(self.x, self.y, 120, 60)
                self.i_string = "Game over"

            self.surface = BTN_FONT.render(self.i_string, False, (255,255,255))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def render(self):
        pygame.draw.rect(screen, (75,0,130), self.bounds)
#        self.text.draw(screen)

    def interact(self, cur, bica):
        cursor_pos = pygame.mouse.get_pos()
        if (cursor_pos[1] < 60):
            if (185 < cursor_pos[0] < 305):
                cur.state = 'TICKLE'
                cur.sprite = pygame.image.load("imgs/arm-tickle.png")
            elif (310 <= cursor_pos[0] < 430):
                cur.state = 'CARESS'
                cur.sprite = pygame.image.load("imgs/arm-caress.png")
            elif (435 <= cursor_pos[0] < 555):
                cur.state = 'THREATEN'
                cur.sprite = pygame.image.load("imgs/arm-boot.png")
            elif (555 <= cursor_pos[0] < 680):
                cur.state = 'COMMAND'
                cur.sprite = pygame.image.load("imgs/arm-command.png")
            elif (1240 <= cursor_pos[0] < 1365):
                cur.state = 'GAME_OVER'
            else:
                cur.state = 'FREE'
                cur.sprite = pygame.image.load("imgs/hand.png")

        else:
            cur.state = 'FREE'
            cur.sprite = pygame.image.load("imgs/hand.png")


class Cursor(pygame.sprite.Sprite):
    states = ['FREE', 'FISH', 'BOOT', 'BALL', 'TICKLE', 'PET', 'THREATEN', 'COMMAND', 'GAME_OVER']
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load("imgs/hand.png")
        self.state = 'FREE'
        self.reward = [0, 0, 0, 0]
        self.i_string = "Pinja is walking"

    def render(self):
        screen.blit(self.sprite, pygame.mouse.get_pos())

    def getPath(self, ob, state, arcs):
        new_state = ob.state
        stt_stck = []
        if new_state in arcs[state]:
            '''if pen.next_state != pen.state:
                    stt_stck.append([pen.state, new_state])
                else:'''
            stt_stck.append([new_state])
            ''' elif new_state in pen.arcs[pen.prev_state]:
                pen.next_state_stack.append(pen.prev_state)
                pen.next_state_stack.append(new_state)'''
        else:
            for st1 in arcs[state][:3]:
                if new_state in arcs[st1]:
                    stt_stck.append([st1, new_state])
                else:
                    for st2 in arcs[st1][:3]:
                        if new_state in arcs[st2]:
                            stt_stck.append([st1, st2, new_state])
        return optimal_path(stt_stck)

    def interact(self, pen, game_objs, console, score, bica, logger):
        cursor = pygame.mouse.get_pos()
        x, y = cursor[0], cursor[1]
        if (pen.get_rect().collidepoint(x, y)):
            if ((abs(x - (pen.x + pen.width / 2)) < INTERACT_DISTANCE) and (
                    abs(y - (pen.y + pen.height - 24)) < INTERACT_DISTANCE)):
     #           new_score = []
     #           for i in range(len(score)):
                if self.state == 'FREE':
                    self.reward = [ 0, 0, 0, 0]
                    self.i_string = "You canceled your action. Pinja is walking"
                elif self.state == 'FISH':
                    self.reward = [+5, 0,+3, +3]
                    bica.interact("fish", True)
                    if bica.pen_accepts:
                        self.i_string = "You fed Pinja and he likes it"
                    else:
                        self.i_string = "Pinja refuses to eat"
                elif self.state == 'BALL':
                    self.reward = [-3,-5,+5, +5]
                    bica.interact("ball", True)
                    if bica.pen_accepts:
                        self.i_string = "You have played a ball with Pinja"
                    else:
                        self.i_string = "Pinja doesn't want to play!"
                elif self.state == 'BOOT':
                    bica.interact("boot", True)
                    if bica.pen_accepts:
                        self.i_string = "You kicked Pinja and he accepted it"
                    else:
                        self.i_string = "You tried to kick Pinja but he ran away"
                    self.reward = [ 0,+2,-7, -7]
                elif self.state == 'TICKLE':
                    bica.interact("tickle", True)
                    if bica.pen_accepts:
                        self.i_string = "You tickled Pinja"
                    else:
                        self.i_string = "Pinja bites you when you tried to tickle him"
                    self.reward = [-1,+2,+5, +4]
                elif self.state == 'CARESS':
                    self.reward = [0, -2, +3, +4]
                    bica.interact("pat", True)
                    if bica.pen_accepts:
                        self.i_string = "You pat Pinja and he is calm"
                    else:
                        self.i_string = "Pinja wouldn't allow you to pat him"
                elif self.state == 'THREATEN':
                    self.reward = [-2, +1, -3, -4]
                    bica.interact("threaten", True)
                    if bica.pen_accepts:
                        self.i_string = "You threated Pinja and he accepted it"
                    else:
                        self.i_string = "You threated Pinja and he doesn't care about"
                else:
                    self.reward = [0, 0, 0, 0]
                stack_hand.append(self.state)
                score = change_score(score, self.reward)
                '''if 0 <= self.reward[i]+score[i] <= 100:
                    new_score.append(self.reward[i]+score[i])
                elif self.reward[i]+score[i] < 0:
                    new_score.append(0)
                elif self.reward[i]+score[i] > 100:
                    new_score.append(100)'''
                #print(self.state)
                #print(score)
                self.state = 'FREE'
                self.sprite = pygame.image.load("imgs/hand.png")
        if self.state == 'COMMAND':
            self.i_string = "You commanded Pinja to go somewhere"
            for ob in game_objs:
                if (ob.get_rect().collidepoint(x, y)):
                    if ((abs(x - (ob.x + ob.width / 2)) < INTERACT_DISTANCE) and (abs(y - (ob.y + ob.height - 24)) < INTERACT_DISTANCE)):
                        if pen.next_state is not None:
                            pen.next_state_stack = self.getPath(ob, pen.next_state, pen.arcs)
                        else:
                            pen.next_state_stack = self.getPath(ob, pen.state, pen.arcs)
                        pen.next_state_stack.append('act')
                        pen.commanded = True
                        #print("Commanded: " + pen.next_state_stack[-2])
                        #bica.interact("pat", True)
                        print(pen.state,' ', pen.next_state, ' ', pen.next_state_stack)
                        if (pen.score[-1] >= 80):
                            score = change_score(score, [0,0,0,+2])
                        elif (pen.score[-1] < 30):
                            score = change_score(score, [0, 0, 0, -5])
                        else:
                            pass
        
        logger.add("player",self.state,pen.score)
        console.setMessage(self.i_string)
        return score


class Inventory(pygame.sprite.Sprite):
    states = ['FISH', 'BOOT', 'BALL']
    i_string=''
    def __init__(self, state):
        pygame.sprite.Sprite.__init__(self)
        if state in self.states:
            self.state = state
            if state == 'FISH':
                self.sprite = pygame.image.load("imgs/inv-fish.png")
                self.x, self.y = 0, 0
                self.i_string = "Eto FISH"
                self.reward = [+5, 0, +5, +3]
            if state == 'BOOT':
                self.sprite = pygame.image.load("imgs/inv-boot.png")
                self.x, self.y = 60, 0
                self.i_string = "Eto BOOT"
                self.reward = [0, +2, -7, -8]
            if state == 'BALL':
                self.sprite = pygame.image.load("imgs/inv-ball.png")
                self.x, self.y = 120, 0
                self.i_string = "Eto BALL"
                self.reward = [-3, -5, +5, +5]
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
    def render(self):
        screen.blit(self.sprite, (self.x, self.y))
    def interact(self, cur, bica):
        cursor_pos = pygame.mouse.get_pos()
        if (cursor_pos[1] < 60):
            if (cursor_pos[0] < 60):
                cur.state = 'FISH'
                cur.sprite = pygame.image.load("imgs/arm-fish.png")
            elif (64 <= cursor_pos[0] < 120):
                cur.state = 'BOOT'
                cur.sprite = pygame.image.load("imgs/arm-boot.png")
            elif (128 <= cursor_pos[0] < 180):
                cur.state = 'BALL'
                cur.sprite = pygame.image.load("imgs/arm-ball.png")
            else:
                cur.state = 'FREE'
                cur.sprite = pygame.image.load("imgs/hand.png")
        else:
            cur.state = 'FREE'
            cur.sprite = pygame.image.load("imgs/hand.png")
                

class Penguin(pygame.sprite.Sprite):
    
    def __init__(self, states, arcs, actions):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load("imgs/pen.png")
        self.size = self.width, self.height = self.sprite.get_size()
        self.x, self.y = 1000 - self.sprite.get_width() / 2, 200 - self.sprite.get_height() + 8
        self.score = [50,50,50,50]   # [hunger, energy, fun, hand]
        self.state = "FBH"
        self.next_state = None
        self.prev_state = None
        self.next_state_stack = []
        self.arcs = arcs
        self.states = states
        self.actions = actions
        self.bounds = pygame.Rect(self.x, self.y, self.width, self.height)
        self.commanded = False
    def move_x(self, dx):
        self.x += dx

    def move_y(self, dy):
        self.y += dy

    def move(self, dx, dy):
        self.bounds = self.bounds.move(dx, dy)

    def get_x(self):
        return self.x + self.width / 2

    def get_y(self):
        return self.y + self.height - 8

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        
    def set_coords(self):
        cursor = pygame.mouse.get_pos()
        x, y = cursor[0], cursor[1]

        dx, dy = x - (self.x + self.width / 2), y - (self.y + self.height - 8)
        len = math.sqrt(dx * dx + dy * dy)
        dx = int(MOVE_OFFSET * dx / len)
        dy = int(MOVE_OFFSET * dy / len)
        return (cursor, dx, dy)

    def get_direction(self, cur_state, next_state):
        x = self.states[next_state][0] - self.states[cur_state][0]
        y = self.states[next_state][1] - self.states[cur_state][1]
        dist = math.sqrt(x*x + y*y)
        x = 5*x / dist
        y = 5*y / dist
        result = (x,y)
        return result

    def move_to_state(self, new_state, game_objects, console, bica, logger):
        if new_state != "act":
#            print(new_state)
            vect = self.get_direction(self.state, new_state)
            vect_len = math.sqrt(vect[0] ** 2 + vect[1] ** 2)
            dist = math.sqrt(
                (self.states[new_state][0] - self.get_x()) ** 2 + (self.states[new_state][1] - self.get_y()) ** 2)
#            print(vect_len, dist)

            if vect_len >= dist:
                self.move_x(self.states[new_state][0] - self.get_x())
                self.move_y(self.states[new_state][1] - self.get_y())
                self.state = new_state
                logger.add("penguin","moved to "+new_state,self.score)
                self.next_state = None
            elif vect_len < dist:
                if ((vect[1] < 0) and (abs(vect[1]) > abs(vect[0]))):
                    self.sprite = pygame.image.load("imgs/pen_back.png")
                elif ((vect[1] > 0) and (abs(vect[1]) > abs(vect[0]))):
                    self.sprite = pygame.image.load("imgs/pen.png")
                elif ((vect[0] > 0) and (abs(vect[1]) < abs(vect[0]))):
                    self.sprite = pygame.image.load("imgs/pen_right.png")
                elif ((vect[0] < 0) and (abs(vect[1]) < abs(vect[0]))):
                    self.sprite = pygame.image.load("imgs/pen_left.png")
                else:
                    pass
                self.move_x(vect[0])
                self.move_y(vect[1])
                self.next_state = new_state
                self.prev_state = self.state

        else:
            self.next_state = None
            if self.state in GameObject.states:
                for g in game_objects:
                    if g.state == self.state:
                        print(self.state)
                        if self.commanded:
                            if bica.pen_accepts:
                                self.score = g.interact(console, self.score, bica, logger, self.commanded)
                            else:
                                console.setMessage("Pinja refuses to lead your commands")
                            self.commanded = False
                        else:
                            self.score = g.interact(console, self.score, bica, logger, self.commanded)
                        print(self.score)


    def getPath(self, new_state, state, arcs):
        stt_stck = []
        if new_state in arcs[state]:
            '''if pen.next_state != pen.state:
                    stt_stck.append([pen.state, new_state])
                else:'''
            stt_stck.append([new_state])
            ''' elif new_state in pen.arcs[pen.prev_state]:
                pen.next_state_stack.append(pen.prev_state)
                pen.next_state_stack.append(new_state)'''
        else:
            for st1 in arcs[state][:3]:
                if new_state in arcs[st1]:
                    stt_stck.append([st1, new_state])
                else:
                    for st2 in arcs[st1][:3]:
                        if new_state in arcs[st2]:
                            stt_stck.append([st1, st2, new_state])
        return optimal_path(stt_stck)
        
    def move_with_probability(self, game_objects, console, new_state_code, bica, logger):
        states = ['matress', 'hill', 'cave', 'food', 'balls']
        if self.next_state == None:
            if len(self.next_state_stack) == 0:
                state_moves = {i: bica.get_distance_after(i, False) for i in states}
                mean = 0.0
                for i in state_moves.values():
                    mean += i 
                mean /= len(states)
                states_to_move = [i for i in states if state_moves[i] < mean]
                new_state = self.state
                i = 5
                while new_state == self.state:
                    new_state = states_to_move[random.randint(0,len(states_to_move)-1)]
                    i -= 1
                    if i < 0:
                        new_state = states[random.randint(0,len(states)-1)]
                self.next_state_stack.extend(self.getPath(new_state, self.state, self.arcs) + ['act'])
                print(self.next_state_stack[0])
            stt = self.next_state_stack.pop(0)
            new_state_code = self.arcs[self.state].index(stt)  # индекс состояния в списке след.состояний текущего состояния
            if new_state_code is None:
                new_state_code = random.randint(0, len(self.arcs[self.state]) - 1)
            add_action(new_state_code)
            self.move_to_state(self.arcs[self.state][new_state_code], game_objects, console, bica, logger)
        else:
            self.move_to_state(self.next_state, game_objects, console, bica, logger)
    '''
    def mouse_move(self, states, cursor, dx, dy):
        cursor = pygame.mouse.get_pos()
        x, y = cursor[0], cursor[1]
        for state in states.keys():
            if (maze.get_rect(state).collidepoint(x, y)):
                self.move_to_state(state)

        if (self.is_free(dx,dy)):
            if (abs(cursor[0] - (self.x + self.width/2)) > MOVE_OFFSET):
                self.move_x(dx)
            if (abs(cursor[1] - (self.y + self.height - 24)) > MOVE_OFFSET):
                self.move_y(dy)'''

    def render(self):
        screen.blit(self.sprite, (self.x, self.y))

    def interact(self, game_objects, game_inventory, game_buttons, cur, console, bica, logger):
        cursor = pygame.mouse.get_pos()
        x, y = cursor[0], cursor[1]
        '''for ob in game_objects:
            if ob.sprite is not None:
                if (ob.get_rect().collidepoint(x, y)):
                    width = ob.sprite.get_width()
                    height = ob.sprite.get_height()
                    if ((abs(ob.x + width / 2 - (self.x + self.width / 2)) < width / 2 + INTERACT_DISTANCE) and (
                            abs(ob.y + height / 2 - (self.y + self.height - 24)) < height / 2 + INTERACT_DISTANCE)):
                        ob.interact(self.score)'''
        self.score = cur.interact(self, game_objects, console, self.score, bica, logger)
        if x <= 180:
            for ob in game_inventory:
                ob.interact(cur, bica)
        else:
            for ob in game_buttons:
                ob.interact(cur, bica)


class Maze(base.PyGameWrapper):

    def __init__(self,  width, height):
        self.states = {"cave": (100,240),
                       "matress": (130,340),
                       "CM": (180,260),
                       "FBH": (1000,200),
                       "food": (1185,277),
                       "BH": (1130,370),
                       "hill": (1000,450),
                       "balls": (1175,640)}
        self.arcs = {"cave": ["CM", "hill", "matress", "act"],
                    "matress": ["cave", "CM", "food", "act"],
                    "CM": ["FBH", "matress", "cave", "act"],
                    "FBH": ["food", "BH", "CM", "act"],
                    "food": ["balls", "matress", "FBH", "act"],
                    "BH": ["FBH", "balls", "hill", "act"],
                    "hill": ["BH", "balls", "cave", "act"],
                    "balls": ["food", "hill", "BH", "act"]}
        self.actions = {"MOVE1": K_q,
                        "MOVE2": K_w,
                        "MOVE3": K_e,
                        "INTERACT": K_r}
        self.nb_actions = len(self.actions)
        base.PyGameWrapper.__init__(self, width, height, actions=self.actions)
        self.init()

    def render(self):
        RED = (255,0,0)
        pygame.draw.line(screen, RED, self.states["cave"], self.states["CM"], 2)
        pygame.draw.line(screen, RED, self.states["matress"], self.states["CM"], 2)
        pygame.draw.line(screen, RED, self.states["FBH"], self.states["CM"], 2)
        pygame.draw.line(screen, RED, self.states["food"], self.states["FBH"], 2)
        pygame.draw.line(screen, RED, self.states["FBH"], self.states["BH"], 2)
        pygame.draw.line(screen, RED, self.states["hill"], self.states["BH"], 2)
        pygame.draw.line(screen, RED, self.states["balls"], self.states["BH"], 2)

        pygame.draw.line(screen, RED, self.states["cave"], self.states["hill"], 2)
        pygame.draw.line(screen, RED, self.states["cave"], self.states["matress"], 2)
        pygame.draw.line(screen, RED, self.states["matress"], self.states["food"], 2)
        pygame.draw.line(screen, RED, self.states["hill"], self.states["balls"], 2)
        pygame.draw.line(screen, RED, self.states["food"], self.states["balls"], 2)
        
    def get_direction(self, cur_state, next_state):
        x = self.states[next_state][0] - self.states[cur_state][0]
        y = self.states[next_state][1] - self.states[cur_state][1]
        dist = math.sqrt(x*x + y*y)
        x = 5*x / dist
        y = 5*y / dist
        result = (x,y)
        return result

    def getScore(self):
        return self.score

    def getGameState(self):
        """
        Gets a non-visual state representation of the game.
        Returns state dict
        -------
        """
        state = {
            "pen_hunger": self.pen.score[0],
            "pen_sleep": self.pen.score[1],
            "pen_fun": self.pen.score[2],
            "pen_hand": self.pen.score[3]
        }

        return state

    def game_over(self):
        return self.is_game_over

    def init(self):
        print("=== Experiment starts ===")
        self.tact = 0
        self.bica = Bica()
    #    self.times_good = 0  # если score дердится на максимуме n тиков, то game over через 2 минуты
    #    self.times_bad = 0   # если score слишком низкий
        self.is_game_over = False
        self.score = 50
        self.background = pygame.image.load("imgs/background.png")
        self.game_objects = [GameObject(st) for st in GameObject.states]
    #    self.game_scales = [Scale(st) for st in Scale.states]
        self.game_inventory = [Inventory(st) for st in Inventory.states]
        self.game_buttons = [Button(st) for st in Button.states]
        self.pen = Penguin(self.states, self.arcs, self.actions)

        self.console = Console()
        self.logger = Logger("exper_" + str(int(time())) + ".csv", self.bica)
        self.cur = Cursor()
        self.pen.score = [50,50,50,50]
        self.timer = time()
        stack = []
        stack_hand = []
        objects = {"cave":0,"matress":0,"CM":0,"FBH":0,"food":0,"BH":0,"hill":0,"balls":0}

    def reset(self):
        if self.is_game_over:
            self.logger.add("player","game_over",self.pen.score)
            self.logger.close()
            self.timer = time() - self.timer
            window.blit(GAME_OVER, (0,0))
            pygame.display.update()
            res_file = open(RESULTS_FILE, "a")
            res_file.write(str(stack))
            res_file.write(str(stack_hand))
            res_file.write(str(objects))
            res_file.write(str(self.pen.score))
            res_file.write(str(self.timer))
            res_file.write("=== Experiment ends ===\n\n")
            res_file.close()
        else:
            self.logger.add("player","reset",self.pen.score)
            self.logger.close()
            self.init()

    def step(self, dt):
        self.tact += 1
        if not self.is_game_over:
            if self.tact % 100 == 0:
                self.pen.score = change_score(self.pen.score, [-1,-1,-1,0])
            '''if self.score==100:
                self.times_good += 1
            elif (self.score < 20):
                self.times_bad += 1
            else:
                self.times_good = 0
                self.times_bad = 0
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    maze.pen.move_x(-MOVE_OFFSET)
                if keys[pygame.K_d]:
                    self.pen.move_x(MOVE_OFFSET)
                if keys[pygame.K_w]:
                    self.pen.move_y(-MOVE_OFFSET)
                if keys[pygame.K_s]:
                    self.pen.move_y(MOVE_OFFSET)'''
            new_state_code = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == RIGHT:
                        if (self.cur.state == 1):
                            coords = self.pen.set_coords()
                        else:
                            self.cur.state = 1
                            self.cur.sprite = pygame.image.load("imgs/hand.png")
                    if event.button == LEFT:
                        self.pen.interact(self.game_objects, self.game_inventory, self.game_buttons, self.cur, self.console, self.bica, self.logger)
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == self.actions['MOVE1']:
                        new_state_code = 0
                    if key == self.actions['MOVE2']:
                        new_state_code = 1
                    if key == self.actions['MOVE3']:
                        new_state_code = 2
                    if key == self.actions['INTERACT']:
                        new_state_code = 3

            #    if (coords != (0,0,0)):
            #        pen.mouse_move(self.states, *coords)

            self.pen.move_with_probability(self.game_objects, self.console, new_state_code, self.bica, self.logger)

            scale_null=False
            '''for i in range(len(self.pen.score)):
                if self.pen.score[i] == 0:
                    scale_null = True'''

            if scale_null or(self.cur.state == 'GAME_OVER'):
                self.is_game_over = True

            screen.blit(self.background, self.background.get_rect())
            for go in self.game_objects:
                go.render()
            '''for go in self.game_scales:
                go.render(self.pen)'''
            for go in self.game_inventory:
                go.render()
            for go in self.game_buttons:
                go.render()


            self.pen.render()
            self.cur.render()

            #self.render()       # no need to render, all works fine. debug only

            window.blit(screen, (0, 0))
            self.console.render()
            for go in self.game_buttons:
                window.blit(go.surface, (go.x + 30, go.y + 24))
            pygame.display.flip()
        else:
            self.is_game_over = True
            self.reset()


if __name__ == "__main__":
    fps = 60
    pygame.init()

    maze = Maze(1366, 768)
    maze.rng = np.random.RandomState(24)
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    maze.clock = pygame.time.Clock()
    maze.init()

    while True:
        dt = maze.clock.tick(fps)
        if maze.game_over():
            maze.reset()
            pygame.quit()

        maze.step(dt)
        pygame.display.update()
        pygame.display.update()