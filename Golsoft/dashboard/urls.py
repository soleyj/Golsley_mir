from django.urls import path
from dashboard import views
from MIR_API import APIs_Manager

app_name = 'basic_app'
APIs_Manager.start()
urlpatterns = [
    path(r'robot',views.RobotsListView.as_view(),name='list'),
    path(r'missions', views.MissionsListView.as_view(), name='misisons'),
    path(r'get_more_tables', views.get_more_tables.as_view(), name='get_more_tables'),
    path(r'change_state', views.change_state, name='change_state'),
    path(r'get_new_missions', views.get_new_missions, name='get_new_missions'),
    path(r'add_mission_url', views.add_mission_url, name='add_mission_url'),
    path(r'cancel_mission_url', views.cancel_mission_url, name='cancel_mission_url'),
]