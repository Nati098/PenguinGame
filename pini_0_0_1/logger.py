from time import *

class Logger:
    def __init__(self, filename):
        self.file = open(filename, 'a')
        self.timestamp = clock()
        self.file.write('Time,Actor,Action,Hunger,Energy,Fun,Rel\n')
    def add(self, actor, action, params):
        st = "{0:.3f}".format(clock()) + "," + actor + "," + action + ","
        st = st + (str(params[0]) + "," + str(params[1]) + "," + str(params[2]) + "," + str(params[3]) + "\n")
        self.file.write(st)
    def close(self):
        self.file.close()