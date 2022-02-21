from django.shortcuts import render
from rest_framework import generics
from .serializers import GPUSerializer
from showgpu.models import GPU
from showgpu.views import filtration
# Create your views here.



class GPUList(generics.ListAPIView):
    def get_queryset(self):
        return filtration(self.request)
    serializer_class = GPUSerializer
    