from django.contrib import admin
from dashboard.models import RStatus,Robot,Mission_queue,Missions
# Register your models here.
admin.site.register(Robot)
admin.site.register(RStatus)
admin.site.register(Mission_queue)
admin.site.register(Missions)