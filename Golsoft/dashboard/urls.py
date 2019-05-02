from django.urls import path
from dashboard import views
from MIR_API import APIs_Manager

app_name = 'basic_app'
APIs_Manager.start()
urlpatterns = [
    ## generla views
    path(r'robot',views.RobotsListView.as_view(),name='list'),
    path(r'missions', views.MissionsListView.as_view(), name='misisons'),
    path(r'configuration', views.configuration.as_view(), name='configuration'),
    path(r'get_more_tables', views.get_more_tables.as_view(), name='get_more_tables'),
    ## robot show view
    path(r'change_state', views.change_state, name='change_state'),
    ## missions views
    path(r'get_new_missions', views.get_new_missions, name='get_new_missions'),
    path(r'add_mission_url', views.add_mission_url, name='add_mission_url'),
    path(r'cancel_mission_url', views.cancel_mission_url, name='cancel_mission_url'),
    ## missions views
    path(r'enter_robot_data', views.enter_robot_data, name='enter_robot_data'),
    path(r'remove_robot_data', views.remove_robot_data, name='remove_robot_data'),

    ## statistics views
    path(r'statistics', views.statistics.as_view(), name='statistics'), 
]