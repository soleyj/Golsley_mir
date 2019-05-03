import requests

version = "/api/v2.0.0/"






### FUNCIONS GENERIQUES

def get_json(robot_ip,auth,path):
    url = robot_ip + version + path
    headers = {'Authorization': auth, 'Content-Type':'application/json'} 
    r = requests.get(url, headers=headers)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None
    
def put_json(robot_ip,auth,path,body):
    url = robot_ip + version + path
    headers = {'Authorization': auth, 'Content-Type':'application/json'}
    r = requests.put(url, headers=headers,json = body)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

def post_json(robot_ip,auth,path,body):
    url = robot_ip + version + path
    print(url)
    headers = {'Authorization': auth, 'Content-Type':'application/json'}
    r = requests.post(url, headers=headers,json = body)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

def delete_json(robot_ip,auth,path):
    url = robot_ip + version + path
    headers = {'Authorization': auth, 'Content-Type':'application/json'}
    r = requests.delete(url, headers=headers)
    try:
        r.raise_for_status()
        return r.json()
    except:
        return None

### FUNCIONS ESPECIFIQUES

def get_robot_status(robot_ip,auth):
    json = get_json(robot_ip,auth,"status")
    if json is not None:
        try:
            return json
        except:
            return None
            pass

def put_state_id(robot_ip,auth,status): #0 for pause 1 for ready
    if(status == 0):
        status = 4
    elif(status == 1):
        status = 3
    else:
        pass 
    json = put_json(robot_ip,auth,"status",{"state_id":status})
    if json is not None:
        try:
            return json
        except:
            return None
            pass


def get_missions(robot_ip,auth):
    json = get_json(robot_ip,auth,"missions")
    if json is not None:
        try:
            return json
        except:
            return None
            pass
    
def get_mission_queue(robot_ip,auth):
    json = get_json(robot_ip,auth,"mission_queue")
    if json is not None:
        try:
            return json
        except:
            return None
            pass
    
def post_new_mission(robot_ip,auth,mission_id):
    json = post_json(robot_ip,auth,"mission_queue/",{"mission_id":mission_id})
    if json is not None:
        try:
            return json
        except:
            return None
            pass


## TEST

# while(1):

# ip = "http://192.168.1.151"
# auth = "Basic ZGlzdHJpYnV0b3I6NjJmMmYwZjFlZmYxMGQzMTUyYzk1ZjZmMDU5NjU3NmU0ODJiYjhlNDQ4MDY0MzNmNGNmOTI5NzkyODM0YjAxNA=="

# print(post_new_mission(ip,auth,"d36d7a03-6d88-11e9-b832-b8aeed74d094"))