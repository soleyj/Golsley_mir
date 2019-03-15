"""
FUNCIONS:
1. Crea les request periòdiques
2. Gestiona totes les request i executa les pendents

JOB: {'name': 'nomjob', 'priority' : 'HIGH/MED/LOW', 'data' : { 'robot' : robot ...}}
"""
from tools import Scheduler
from tools import jobs_to_methods

status_scheduler = Scheduler('get_status',100, 'LOW')
PLC_scheduler = Scheduler('get_PLC',100, 'LOW')
Schedulers_list=[status_scheduler,PLC_scheduler]

Job_list = []

def mir_api_main():
    global Job_list
    while(True):
        Update()
        Run_Next_Job()


def Update():
    global Job_list
    for sched in Schedulers_list:
        sched.run()
    h=[]
    m=[]
    l=[]
    for job in Job_list:
        if job['priority'] == 'HIGH':
            h.append(job)
        elif job['priority'] == 'MID':
            m.append(job)
        elif job['priority'] == 'LOW':
            l.append(job)
        else:
            pass
    Job_list=h+m+l

def Run_Next_Job():
    global Job_list
    if len(Job_list) > 0:
        job = Job_list.pop(0)
        method = jobs_to_methods.get(job['name'])
        return method(job['data'])

def Add_Job(name, robot, value = None, priority = 'HIGH'):
    global Job_list
    Job_list.append({'name': name, 'priority' : priority, 'data' : { 'robot' : robot, 'value' : value}})
