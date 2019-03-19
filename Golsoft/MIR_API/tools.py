from time import time
from . import MIR_API


class Scheduler:

    def __init__(self,name, interval):
        self.name = name
        self.interval = interval
        self.last_time = 0


    def run(self):
        if time() >  self.last_time + self.interval:
            self.name()
            self.last_time =time()
        else:
            pass
