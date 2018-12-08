from time import *

class Logger:
    def __init__(self, filename, bica):
        self.file = open(filename, 'a')
        self.timestamp = clock()
        self.file.write('Time,Actor,Action,Hunger,Energy,Fun,Rel,Pen_Val,Pen_Dom,Hand_Val,Hand_Dom\n')
        self.bica = bica
    def add(self, actor, action, params):
        st = "{0:.3f}".format(clock()) + "," + actor + "," + action + ","
        st = st + (str(params[0]) + "," + str(params[1]) + "," + str(params[2]) + "," + str(params[3]) + ",")
        st = st + (str(self.bica.pen_state[0]) + "," + str(self.bica.pen_state[1]) + ",")
        st = st + (str(self.bica.hand_state[0]) + "," + str(self.bica.hand_state[1]) + "\n")
        self.file.write(st)
    def close(self):
        self.file.close()