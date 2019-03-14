from django.db import models
from datetime import datetime

# Create your models here.
class Robot(models.Model):
    model= models.CharField(max_length=150,default = "none")
    robot_name = models.CharField(max_length=150,default = "none")
    auth = models.CharField(max_length=150,default = "none")
    ip = models.CharField(max_length=150,default = "none")

    def __str__(self):
        return self.robot_name

class RStatus(models.Model):
    robot = models.ForeignKey(Robot, related_name='robot', on_delete=models.CASCADE,default = 1)
    battery = models.DecimalField(max_digits=12,decimal_places=2,default = 1)
    posx = models.DecimalField(max_digits=12,decimal_places=2,default = 1)
    posy = models.DecimalField(max_digits=12,decimal_places=2,default = 1)
    orientation = models.DecimalField(max_digits=12,decimal_places=2,default = 1)
    state1 = models.CharField(max_length=150,default = "none")
    velocity_l = models.DecimalField(max_digits=12,decimal_places=2,default = 1)
    velocity_a = models.DecimalField(max_digits=12,decimal_places=2,default = 1)

    def __str__(self):
        return self.state