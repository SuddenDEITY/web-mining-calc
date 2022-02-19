from django.shortcuts import render
from .models import GPU_Type
from django.views.generic.list import ListView


class GPU_Type_List(ListView): #returns list of GPU_Type objects
    model = GPU_Type
    template_name = 'showgpu/gpu_type_list.html'
    context_object_name = 'gpu_type_list'
