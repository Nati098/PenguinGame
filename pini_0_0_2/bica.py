import math


class Bica:
    R = 0.01              # model parameter from "Samsonovich, 2013" paper
    pen_state = [0,-1] # valence, dominance
    hand_state = [0,1]
    
    pen_accepts = True
    
    def __init__(self):
        pass
    
    ''' Возвращает вектор смещения при выполнении действия
        и условии подчинения пингвина '''
    def get_change_by_action(self, act, pen_accepts):
        new_pen_state = [0,0]
        new_hand_state = [0,0]
        if act == "boot":
            new_pen_state[0] = -4.0
            new_pen_state[1] = -2.5
            if pen_accepts:
                new_hand_state[0] = 0.5
                new_hand_state[1] = 4.58
            else:
                new_hand_state[0] = -1
                new_hand_state[1] = 0.25
        elif act == "fish":
            new_pen_state[0] = 4.25
            new_pen_state[1] = -0.42
            if pen_accepts:
                new_hand_state[0] = 2.58
                new_hand_state[1] = 2.08
            else:
                new_hand_state[0] = -0.67
                new_hand_state[1] = -0.67
        elif act == "balls":
            new_pen_state[0] = 3.67
            new_pen_state[1] = 1.5
            if pen_accepts:
                new_hand_state[0] = 4.0
                new_hand_state[1] = 2.5
            else:
                new_hand_state[0] = -0.5
                new_hand_state[1] = -0.67
        elif act == "tickle":
            new_pen_state[0] = 1.58
            new_pen_state[1] = -0.08
            if pen_accepts:
                new_hand_state[0] = 3.08
                new_hand_state[1] = 3.5
            else:
                new_hand_state[0] = -1.25
                new_hand_state[1] = -0.92
        elif act == "pat":
            new_pen_state[0] = 2.83
            new_pen_state[1] = -0.83
            if pen_accepts:
                new_hand_state[0] = 4.0
                new_hand_state[1] = 2.33
            else:
                new_hand_state[0] = -1.25
                new_hand_state[1] = -0.5
        elif act == "threaten":
            new_pen_state[0] = -2.83
            new_pen_state[1] = -1.25
            if pen_accepts:
                new_hand_state[0] = 0.5
                new_hand_state[1] = 3.75
            else:
                new_hand_state[0] = -2.16
                new_hand_state[1] = 0.33
        elif act == "hill":
            new_pen_state[0] = 0.17
            new_pen_state[1] = -1.08
            if pen_accepts:
                new_hand_state[0] = 1.67
                new_hand_state[1] = 2.41
            else:
                new_hand_state[0] = -1.75
                new_hand_state[1] = -0.67
        elif act == "matress":
            new_pen_state[0] = 0.83
            new_pen_state[1] = -0.25
            if pen_accepts:
                new_hand_state[0] = 1.67
                new_hand_state[1] = 2.41
            else:
                new_hand_state[0] = -1.75
                new_hand_state[1] = -0.67
        elif act == "cave":
            new_pen_state[0] = -0.5
            new_pen_state[1] = -0.92
            if pen_accepts:
                new_hand_state[0] = 1.67
                new_hand_state[1] = 2.41
            else:
                new_hand_state[0] = -1.75
                new_hand_state[1] = -0.67
        elif act == "wake":
            new_pen_state[0] = -2.33
            new_pen_state[1] = -0.17
            if pen_accepts:
                new_hand_state[0] = 1.67
                new_hand_state[1] = 2.41
            else:
                new_hand_state[0] = -2.08
                new_hand_state[1] = 0.08
        elif act == "food":
            new_pen_state[0] = 4.17
            new_pen_state[1] = -0.33
            if pen_accepts:
                new_hand_state[0] = 1.67
                new_hand_state[1] = 2.41
            else:
                new_hand_state[0] = -1.75
                new_hand_state[1] = -0.67
        elif act == "hid":
                new_hand_state[0] = -1.08
                new_hand_state[1] = 0.17
        return (new_pen_state, new_hand_state)        
        
    ''' Нужно вызывать при взаимодействии, чтобы поменять 
        эмоциональные оценки человека и пингвина '''
    def interact(self, act, command=True):    
        new_states = self.get_change_by_action(act, self.pen_accepts)
        self.pen_state[0]  = (1-self.R)*self.pen_state[0]  + self.R*new_states[0][0]
        self.pen_state[1]  = (1-self.R)*self.pen_state[1]  + self.R*new_states[0][1]
        if command:
            self.hand_state[0] = (1-self.R)*self.hand_state[0] + self.R*new_states[1][0]
            self.hand_state[1] = (1-self.R)*self.hand_state[1] + self.R*new_states[1][1]
        self.set_acceptance()

    ''' Проверяет, будет ли пингвин подчиняться приказам, или сопротивляться им '''
    def set_acceptance(self):
        if self.pen_state[0] < -0.5:
            self.pen_accepts = False
        elif self.pen_state[0] > +0.5:
            self.pen_accepts = True
       
    ''' Позволяет узнать, изменится ли отношение пингвина к взаимодействию 
        после выполнения действия '''
    def get_acceptance(self, act):
        new_states = self.get_change_by_action(act, self.pen_accepts)
        if (1-self.R)*self.pen_state[0]  + self.R*new_states[0][0] < -15:
            return False
        elif (1-self.R)*self.pen_state[0]  + self.R*new_states[0][0] > +10:
            return True
        else:
            return self.pen_accepts
        
    def vector_distance(self, v1, v2):
        return math.sqrt((v1[0]-v2[0])**2 + (v1[1]-v2[1])**2)
        
    ''' Позволяет вычислить расстояние между новыми состояниями 
        пингвина и руки'''
    def get_distance_after(self, act, command=False):
        new_states = self.get_change_by_action(act, self.get_acceptance(act))
        pen_new = [(1-self.R)*self.pen_state[0]+self.R*new_states[0][0], (1-self.R)*self.pen_state[1]+self.R*new_states[0][1]]
        if command:
            hand_new = [(1-self.R)*self.hand_state[0]+self.R*new_states[1][0], (1-self.R)*self.hand_state[1]+self.R*new_states[1][1]]
        else:
            hand_new = self.hand_state
        return self.vector_distance(pen_new, hand_new)
        
    
        
    def get_current_distance(self):
        return self.vector_distance(self.pen_state, self.hand_state)
        
    def get_current_distance(self):
        return self.vector_distance(self.pen_state, self.hand_state)
        
    
        