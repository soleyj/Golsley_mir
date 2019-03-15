'''
FUNCIONS
1.Fa crides als sitemes (Robot, PLC...)
2.Enregistra les respostes
'''

from dashboard.models import Robot
from dashboard.models import RStatus
from dashboard.models import Missions
from . import Driver_MIR


def get_robot_info(data):

    json = Driver_MIR.get_robot_status(data['robot'].ip, data['robot'].auth)

    if json is not None:
        try:
            new_robot = Robot()
            new_robot.model = json['robot_model']
            new_robot.name = json['robot_name']
            new_robot.ip = data['robot'].ip
            new_robot.auth = data['robot'].auth
            new_robot.save()
        except:
            pass


def get_status(data):

    json = Driver_MIR.get_robot_status(data['robot'].ip, data['robot'].auth)

    if json is not None:
        try:
            new_rstatus = RStatus()
            new_rstatus.robot  = data['robot']
            new_rstatus.battery  = json['battery_percentage']
            new_rstatus.posx= json['position']['x']
            new_rstatus.posy =json['position']['y']
            new_rstatus.orientation = json['position']['orientation']
            if(json['state_text'] == 4):
                new_rstatus.state1 = 0
            elif(json['state_text'] == 3):
                new_rstatus.state1 = 1
            new_rstatus.velocity_l = json['velocity']['linear']
            new_rstatus.velocity_a = json['velocity']['angular']
            new_rstatus.save()
        except:
            pass


def get_missions(data):
    json = Driver_MIR.get_missions(data['robot'].ip, data['robot'].auth)

    if json is not None:
        try:
            for mission in json:
                new_mission = Missions()
                new_mission.id_mission = mission['id']
                new_mission.name = mission['name']
                new_mission.url = mission['url']
                new_mission.save()
        except:
            pass


def get_mission_queue(data):
    json = Driver_MIR.get_mission_queue(data['robot'].ip, data['robot'].auth)

    if json is not None:
        try:
            new_mission_queue = Mission_queue()
            new_mission_queue.mission = Missions.objects.all()(json['241']['id'])  # REVISAR
            new_mission_queue.asigned_robot = data['robot']
            new_mission_queue.url = json['url']
            new_mission_queue.save()
        except:
            pass

def put_state(data):

    Driver_MIR.put_state_id(data['robot'].ip, data['robot'].auth,data['value'])
    get_status(data)
