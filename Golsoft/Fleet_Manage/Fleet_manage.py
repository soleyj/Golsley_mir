##Module to control the logic of the robots fleet.
from MIR_API import APIs_Manager
from dashboard.models import Robot, RStatus , Mission_queue

## USEFUL FUNCITONS.
# APIs_Manager.check_free_robots(), return an array of the ID of free robots.
# APIs_Manager.Mission_to_Robot(ROBOT ID, MISSIOn ID) assig a mission ID from mission Queue to a Robot ID. (Add new job to API)
#
#

def Update_fleet_manage():
    FIFO_MANAGE()




def FIFO_MANAGE():
    free_robots = APIs_Manager.check_free_robots()
    for robots in free_robots:
        mission_id = Mission_queue.objects.filter(mision_state = 0).order_by('time_request').first()
        if(mission_id):
            APIs_Manager.Mission_to_Robot(robots,mission_id.id)  


## can be write a costum manage of robot Fleet!!!
def Custom_Manage():
    pass