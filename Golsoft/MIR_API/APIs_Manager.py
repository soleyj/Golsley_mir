"""
FUNCIONS:
1. Crea les request periòdiques
2. Gestiona totes les request i executa les pendents

JOB: {'name': 'nomjob', 'priority' : 'HIGH/MED/LOW', 'data' : { 'robot' : robot ...}}
"""

from . import tools
from dashboard.models import Robot, RStatus , Mission_queue
from . import MIR_API
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pprint import pprint


jobs_to_methods ={
    'get_status' : MIR_API.get_status,
    'get_robot' : MIR_API.get_robot_info,
    'get_missions' : MIR_API.get_missions,
    'put_state' : MIR_API.put_state,
    'add_new_mission': MIR_API.post_new_mission
}



def start():

    scheduler = BackgroundScheduler()
    scheduler.add_job(mir_api_main, 'interval',seconds = 0.05)
    scheduler.start()
    



def mir_api_main():
    
    global Job_list
    robot = Robot.objects.get(id = 4)
    Update()
     # Run_Next_Job()
    pprint(Job_list)


def Update():
    Ording_priority()
    FIFO_mission_manager()

def Run_Next_Job():
    global Job_list
    if len(Job_list) > 0:
        job = Job_list.pop(0)
        print(job)
        method = jobs_to_methods.get(job['name'])
        return method(job['data'])

def Add_Job(name, robot, value = None, priority = 'HIGH'):
    global Job_list
    Job_list.append({'name': name, 'priority' : priority, 'data' : { 'robot' : robot, 'value' : value}})


def Manager_request_robot_status():
    field = Robot.objects.all()

    for robots in field:
        check_job = 0
        field_=getattr(robots,'id') 
        for job in Job_list:
            if(job['name'] == 'get_status' ):
                if(job['data']['robot'].id  == field_):
                    check_job = 1
        if(check_job == 0):#add new api call if is not in the list!!
            Add_Job('get_status',robots,priority='LOW')




def Ording_priority():
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

def FIFO_mission_manager():
    # check if there are robots able
    field = Robot.objects.all()   
    for robots in field:
        check_job = 0
        robot_id=getattr(robots,'id') 
        robot_state = RStatus.objects.filter(robot__id=str(robot_id)).order_by('-id').first()
        if(robot_state.state == 0):
            check_job = 1
            #now check if this robot has job 
            for job in Job_list:
                if(job['name'] == 'add_new_mission' ):
                    if(job['data']['robot'].id  == robot_id):
                        check_job = 0
            if (check_job == 1):
                ## get the last mission ID
                mission_id = Mission_queue.objects.filter(mision_state = 0).order_by('time_request').first()
                if(mission_id):
                    ## set mission_quee add to the robot in order to reasign the same mission
                    mission_id.mision_state =1
                    mission_id.asigned_robot = robots
                    mission_id.save()
                    Add_Job('add_new_mission',robots, priority='HIGH',value =mission_id.mission.id_mission )















status_scheduler = tools.Scheduler(Manager_request_robot_status,0.05)
Schedulers_list=[status_scheduler]

Job_list = []