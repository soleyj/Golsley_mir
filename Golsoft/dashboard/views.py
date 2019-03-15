from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)

from . import models
from itertools import chain

class IndexView(TemplateView):
    # Just set this Class Object Attribute to the template page.
    # template_name = 'app_name/site.html'
    template_name = 'dashboard/index.html'

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        context['injectme'] = "Basic Injection!"
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

    def get_context_data(self,**kwargs):
        context  = super().get_context_data(**kwargs)
        field = models.Robot.objects.all()
        queryset_list = set()

        for robots in field:
            field_=getattr(robots,'robot_name')
            print(field_)
            queryset_list.add(models.RStatus.objects.filter(robot__robot_name=str(field_)).order_by('-id').first())
            print(queryset_list)


        queryset_list_ = models.RStatus.objects.filter(robot__robot_name=str('Mir_154')).order_by('-id').first()
        context['injectme'] = queryset_list
        print(context)
        return context


