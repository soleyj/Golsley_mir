from time import time
from . import MIR_API

jobs_to_methods ={
    'get_status' : MIR_API.get_status,
    'get_robot' : MIR_API.get_robot_info,
    'get_missions' : MIR_API.get_missions,
    'put_state' : MIR_API.put_state
}
class Scheduler:

    def __init__(self,name, interval, priority):
        self.name = name
        self.interval = interval
        self.priority = priority
        self.last_time = 0


    def run(self,job_list):
        if time() >  self.last_time + self.interval and self.job not in job_list:
            job_list.append({'name': self.name, 'priority' : self.priority})
            self.inlist = 1
            self.last_time = time()
        else:
            pass
