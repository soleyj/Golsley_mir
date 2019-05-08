

import requests
from dashboard.models import GolsBox, Mission_queue, Missions , Robot
from MIR_API import APIs_Manager
last_value_sw = [0,0,0,0]


def get_sw(ip):
    url = ip + "sw"
    r = requests.get(url)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None


def put_sw(ip, data):
    url = ip + "sw"
    headers = {'Content-Type': 'application/json'}
    body = {"id": data}
    r = requests.put(url, headers=headers, json=body)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None


def check_box(id_):
    box = GolsBox.objects.filter(id=id_).get()
    robot = Robot.objects.filter(robot_name = "Mir154").get()
    if(box.SW3_state != last_value_sw[3]):
        if(box.SW3_state ==1 ):
            APIs_Manager.Add_Job("post_register", robot, {"register":100,"value":2})
        else:
            APIs_Manager.Add_Job("post_register", robot,  {"register":100,"value":1})
        pass
    if(box.SW1_mode == 1):
        if(box.SW1_state == 1):
            # add new mission
            Add_box_mission(box, 1)
            box.SW1_state = False
            box.save()
            APIs_Manager.Add_Job("put_box", box, 0)
    if(box.SW2_mode == 1):
        if(box.SW2_state == 1):
            # add new mission
            Add_box_mission(box, 2)
            box.SW2_state = False
            box.save()
            APIs_Manager.Add_Job("put_box", box, 1)
    if(box.SW3_mode == 1):
        if(box.SW3_state == 1):
            # add new mission
            Add_box_mission(box, 3)
            box.SW3_state = False
            box.save()
            APIs_Manager.Add_Job("put_box", box, 2)
    if(box.SW4_mode == 1):
        if(box.SW4_state == 1):
            # add new mission
            Add_box_mission(box, 4)
            box.SW4_state = False
            box.save()
            APIs_Manager.Add_Job("put_box", box, 3)
    pass
    last_value_sw[3] = box.SW3_state 

def Add_box_mission(box, sw):
    # get mission from sw 1
    if(sw == 1):
        mission = box.SW1_mission
    if(sw == 2):
        mission = box.SW2_mission
    if(sw == 3):
        mission = box.SW3_mission
    if(sw == 4):
        mission = box.SW4_mission

    if(mission):
        mission_model = Missions.objects.get(name=mission)

        new = Mission_queue(mission=mission_model, mision_state=0)
        new.save()


def get_box(data):
    json = get_sw(data['robot'].ip)
    
    if json is not None:
        try:
            box_data = GolsBox.objects.get(ip=data["robot"].ip)
            box_data.SW1_mode = json[0]['SW_mode']
            box_data.SW1_state = json[0]['SW_state']
            box_data.SW2_mode = json[1]['SW_mode']
            box_data.SW2_state = json[1]['SW_state']
            box_data.SW3_mode = json[2]['SW_mode']
            box_data.SW3_state = json[2]['SW_state']
            box_data.SW4_mode = json[3]['SW_mode']
            box_data.SW4_state = json[3]['SW_state']
            box_data.verification = True
            box_data.save()
        except:
            box_data = GolsBox.objects.get(ip=data["robot"].ip)
            box_data.verification = False
            pass


def put_box(data):
    json = put_sw(data['robot'].ip, data["value"])
    if json is not None:
        try:
            pass
        except:
            pass
