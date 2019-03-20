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
from Fleet_Manage import Fleet_manage

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
    Fleet_manage.Update_fleet_manage()

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




def check_free_robots():
    # check if there are robots able
    field = Robot.objects.all()  
    free_robot = [] 
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
                free_robot.append(robot_id)

    print(free_robot)
    return free_robot


def Mission_to_Robot(robot_id,mission_id):
    robot = Robot.objects.filter(id = robot_id).get()
    mission = Mission_queue.objects.filter(id=mission_id).get()
    print(mission)
    mission.mision_state = 1
    mission.asigned_robot = robot
    mission.save()
    Add_Job('add_new_mission',robot, priority='HIGH',value =mission.mission.id_mission )









status_scheduler = tools.Scheduler(Manager_request_robot_status,0.05)
Schedulers_list=[status_scheduler]

Job_list = []