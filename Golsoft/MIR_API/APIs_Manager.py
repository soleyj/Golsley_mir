"""
FUNCIONS:
1. Crea les request periòdiques
2. Gestiona totes les request i executa les pendents

JOB: {'name': 'nomjob', 'priority' : 'HIGH/MED/LOW', 'data' : { 'robot' : robot ...}}
"""

from . import tools
from dashboard.models import Robot, RStatus, Mission_queue, GolsBox
from . import MIR_API
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from pprint import pprint
from Fleet_Manage import Fleet_manage
from GolBoxApi import GolBoxApi
import time

jobs_to_methods = {
    'get_status': MIR_API.get_status,
    'get_robot': MIR_API.get_robot_info,
    'get_missions': MIR_API.get_missions,
    'put_state': MIR_API.put_state,
    'add_new_mission': MIR_API.post_new_mission,
    'get_box': GolBoxApi.get_box,
    'put_box': GolBoxApi.put_box,
    'post_register' :MIR_API.post_register,
}


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(mir_api_main, 'interval', seconds=0.5)
    scheduler.start()


def mir_api_main():

    global Job_list
    
    Update()
    Run_Next_Job()
    # pprint(Job_list)


def Update():
    Ording_priority()
    Fleet_manage.Update_fleet_manage()
    

def Run_Next_Job():
    global Job_list
    if len(Job_list) > 0:
        job = Job_list.pop(0)
        method = jobs_to_methods.get(job['name'])
        print(job['name'],job['data']['robot'].id)
        method(job['data'])
        if(job['name']=="get_status"):
            Update_check_RobotsMissions(job['data']['robot'].id)
        if(job['name']=="get_box"):
            GolBoxApi.check_box(job['data']['robot'].id)


def Add_Job(name, robot, value=None, priority='HIGH'):
    global Job_list
    # check if job is already add
    check_job = 1
    for job in Job_list:
        if(job['name'] == name):
            if(job['data']['robot'].id == robot.id):
                if(value == "None"):
                    check_job = 0
                else:
                    if(job['data']['value'] == value):
                        check_job = 0
    if(check_job == 1):
        Job_list.append({'name': name, 'priority': priority,
                         'data': {'robot': robot, 'value': value}})


def Manager_request_robot_status():
    field = Robot.objects.all()
    for robots in field:
        check_job = 0
        field_ = getattr(robots, 'id')
        if(check_job == 0):  # add new api call if is not in the list!!
            if(getattr(robots, 'robot_name') == "none"):
                Add_Job('get_robot', robots, priority='LOW')
            else:
                Add_Job('get_status', robots, priority='LOW')
    
    GolBoxs = GolsBox.objects.all()
    ##check
    for box in GolBoxs:
        Add_Job("get_box", box, priority='LOW')


def Ording_priority():
    global Job_list
    for sched in Schedulers_list:
        sched.run()
    h = []
    m = []
    l = []
    for job in Job_list:
        if job['priority'] == 'HIGH':
            h.append(job)
        elif job['priority'] == 'MID':
            m.append(job)
        elif job['priority'] == 'LOW':
            l.append(job)
        else:
            pass
    Job_list = h+m+l


def check_free_robots():
    field = Robot.objects.all()
    free_robot = []
    for robots in field:
        if robots.verification == True:
            check_job = 0
            robot_id = getattr(robots, 'id')
            robot_state = RStatus.objects.filter(
                robot__id=str(robot_id)).order_by('-id').first()
            if(robot_state):
                if(robot_state.state == 3):
                    check_job = 1
                    missions_available = Mission_queue.objects.filter(
                        asigned_robot__id=str(robot_id)).order_by('-id').first()
                    if(missions_available):
                        if(missions_available.mision_state != 4):
                            check_job = 0
                    if (check_job == 1):
                        free_robot.append(robot_id)

    return free_robot


def Mission_to_Robot(robot_id, mission_id):
    robot = Robot.objects.filter(id=robot_id).get()
    mission = Mission_queue.objects.filter(id=mission_id).get()
    mission.mision_state = 1
    mission.asigned_robot = robot
    mission.save()


def Update_check_RobotsMissions(id_):
    robots = Robot.objects.filter(id=id_).get()
    try:
        if(robots.verification == True):
            rdata = RStatus.objects.filter(
                robot__id=str(robots.id)).order_by('-id').first()
            if(rdata):
                mission = Mission_queue.objects.filter(
                        asigned_robot_id=str(robots.id)).order_by('-id').first()
                if(rdata.state == 3):                  
                    if(mission.mision_state == 1):
                        if(not rdata.mission_queue_id):
                            Add_Job('add_new_mission', robots, priority='HIGH',
                                    value=mission.mission.id_mission)
                    elif(mission.mision_state == 2 and not rdata.mission_queue_id ):
                        mission.mision_state = 4
                        mission.save()
                elif(rdata.state == 5):
                    if(rdata.mission_queue_id and mission.mision_state == 1):
                        mission.mision_state =2
                        mission.save()
    except:
        pass


status_scheduler = tools.Scheduler(Manager_request_robot_status, 0.5)
Schedulers_list = [status_scheduler]

Job_list = []
