from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View, TemplateView,
                                  ListView, DetailView,
                                  CreateView, DeleteView,
                                  UpdateView)

from . import models
from itertools import chain
from MIR_API import APIs_Manager


class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = "GOLSLEY SOFTWARE FOR MIR ROBOTS"
        return context


class Golbox(ListView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'dashboard/golbox.html'

    model = models.GolsBox

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = models.Missions.objects.all()
        print(context)
        return context


class RobotsListView(ListView):
    # If you don't pass in this attribute,
    # Django will auto create a context name
    # for you with object_list!
    # Default would be 'school_list'

    # Example of making your own:
    # context_object_name = 'schools'
    template_name = 'dashboard/robots.html'
    model = models.Robot

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field = models.Robot.objects.all()
        queryset_list = set()

        for robots in field:
            field_ = getattr(robots, 'robot_name')
            print(field_)
            queryset_list.add(models.RStatus.objects.filter(
                robot__robot_name=str(field_)).order_by('-id').first())
            print(queryset_list)

        context['injectme'] = queryset_list
        return context


class MissionsListView(ListView):
    template_name = 'dashboard/Missions.html'
    model = models.Missions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['injectme'] = models.Mission_queue.objects.order_by(
            '-mision_state').all()
        return context


class configuration(ListView):
    model = models.Robot
    template_name = 'dashboard/configuration.html'


class get_more_tables(TemplateView):
    model = models.Robot
    template_name = 'dashboard/get_more_tables.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        field = models.Robot.objects.all()
        queryset_list = set()
        print("hello WOrld AJAX WORKS XD")
        for robots in field:
            field_ = getattr(robots, 'robot_name')
            print(field_)
            queryset_list.add(models.RStatus.objects.filter(
                robot__robot_name=str(field_)).order_by('-id').first())
            print(queryset_list)

        context['injectme'] = queryset_list
        print(context)
        return context


def change_state(request):
    robot_id = int(request.GET['robot_id'])
    robot = models.Robot.objects.get(id=robot_id)
    robot_state = models.RStatus.objects.filter(
        robot__id=str(robot_id)).order_by('-id').first()
    if(robot_state.state == 1):
        APIs_Manager.Add_Job('put_state', robot, 0)
    elif(robot_state.state == 0):
        APIs_Manager.Add_Job('put_state', robot, 1)
    # call the api here with the correct id
    return HttpResponse("OK")


def get_new_missions(request):
    robot_name = "MiR_R165"
    robot = models.Robot.objects.get(robot_name=robot_name)
    APIs_Manager.Add_Job('get_missions', robot)
    print("new Missons")

    # call the api to get new mission list!

    return HttpResponse("OK")


def add_mission_url(request):
    mission_id = str(request.GET['mission_id'])
    mission_model = models.Missions.objects.get(id_mission=mission_id)

    new = models.Mission_queue(mission=mission_model, mision_state=0)
    new.save()
    user_dict_ = models.Mission_queue.objects.order_by('-mision_state').all()
    user_dict = {"injectme": user_dict_}
    print(user_dict)
    return render(request, 'dashboard/Missions_queue.html', context=user_dict)


def cancel_mission_url(request):
    mission_queue_id = int(request.GET['mission_queue_id'])
    mode_mission_queue = models.Mission_queue.objects.get(id=mission_queue_id)
    mode_mission_queue.mision_state = -1
    mode_mission_queue.save()
    user_dict_ = models.Mission_queue.objects.order_by('-mision_state').all()
    user_dict = {"injectme": user_dict_}
    print(user_dict)
    return render(request, 'dashboard/Missions_queue.html', context=user_dict)


def enter_robot_data(request):
    robot_ip = str(request.GET['robot_ip'])
    robot_auth = str(request.GET['robot_auth'])
    new = models.Robot(ip=robot_ip, auth=robot_auth)
    new.save()
    user_dict_ = models.Robot.objects.all()
    user_dict = {"injectme": user_dict_}
    return render(request, 'dashboard/robot_info.html', context=user_dict)


def remove_robot_data(request):
    robot_id = int(request.GET['robot_id'])
    models.Robot.objects.get(id=robot_id).delete()
    user_dict_ = models.Robot.objects.all()
    user_dict = {"injectme": user_dict_}
    print(user_dict)
    return render(request, 'dashboard/robot_info.html', context=user_dict)


class statistics(ListView):

    template_name = 'dashboard/statistics.html'
    model = models.Missions
