from django.db import models
from datetime import datetime
from django.urls import reverse


# Create your models here.
class Robot(models.Model):
    model = models.CharField(max_length=150, default="none")
    robot_name = models.CharField(max_length=150, default="none")
    auth = models.CharField(max_length=150, default="none")
    ip = models.CharField(max_length=150, default="none")
    verification = models.BooleanField(default=False)

    def __str__(self):
        return self.robot_name


class RStatus(models.Model):
    robot = models.ForeignKey(
        Robot, related_name='robot', on_delete=models.CASCADE, default=1)
    battery = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    posx = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    posy = models.DecimalField(max_digits=12, decimal_places=2, default=1)
    orientation = models.DecimalField(
        max_digits=12, decimal_places=2, default=1)
    state = models.IntegerField()  # 1 ready 0 stop
    statetext = models.CharField(
        max_length=150, default="none")  # 1 ready 0 stop
    velocity_l = models.DecimalField(
        max_digits=12, decimal_places=2, default=1)
    velocity_a = models.DecimalField(
        max_digits=12, decimal_places=2, default=1)
    mission_queue_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.robot.robot_name


class Missions(models.Model):
    id_mission = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150, unique=True)
    url = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Mission_queue(models.Model):
    mission = models.ForeignKey(
        Missions, related_name='asigned_mission', on_delete=models.CASCADE)
    asigned_robot = models.ForeignKey(
        Robot, related_name='asigned_robot', on_delete=models.CASCADE, null=True, blank=True)
    mision_state = models.IntegerField()  # 3cancelled 2 executing 1 assigned 0 stop 4 finsh
    robot_queue_id = models.IntegerField(null=True, blank=True)
    time_request = models.DateTimeField(auto_now=True)

    def filter_status(self):
        return self.mision_state.orderby(mision_state).all()

    def __str__(self):
        return self.mission.name


class GolsBox(models.Model):
    ip = models.CharField(max_length=150, default="none")
    verification = models.BooleanField(default=False)
    SW1_mode = models.IntegerField(default=2)  # 0 for interrupt 1 for smart SW
    SW1_state = models.BooleanField(default=False)
    SW2_mode = models.IntegerField(default=2)  # 0 for interrupt 1 for smart SW
    SW2_state = models.BooleanField(default=False)
    SW3_mode = models.IntegerField(default=2)  # 0 for interrupt 1 for smart SW
    SW3_state = models.BooleanField(default=False)
    SW4_mode = models.IntegerField(default=2)  # 0 for interrupt 1 for smart SW
    SW4_state = models.BooleanField(default=False)
    SW1_mission = models.ForeignKey(
        Missions, related_name='asigned_mission1', on_delete=models.CASCADE, null=True, blank=True)
    SW2_mission = models.ForeignKey(
        Missions, related_name='asigned_mission2', on_delete=models.CASCADE, null=True, blank=True)
    SW3_mission = models.ForeignKey(
        Missions, related_name='asigned_mission3', on_delete=models.CASCADE, null=True, blank=True)
    SW4_mission = models.ForeignKey(
        Missions, related_name='asigned_mission4', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.ip
