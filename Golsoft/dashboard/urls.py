from django.urls import path
from dashboard import views

app_name = 'basic_app'

urlpatterns = [
    path(r'robot',views.RobotsListView.as_view(),name='list'),
]
