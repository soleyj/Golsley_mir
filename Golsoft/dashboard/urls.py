from django.urls import path
from dashboard import views

app_name = 'basic_app'

urlpatterns = [
    path(r'robot',views.RobotsListView.as_view(),name='list'),
    path(r'missions', views.MissionsListView.as_view(), name='misisons'),
    path(r'get_more_tables', views.get_more_tables.as_view(), name='get_more_tables'),
    path(r'change_state', views.change_state, name='change_state'),
]
