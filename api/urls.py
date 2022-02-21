from django.urls import path
from .views import GPUList

urlpatterns = [
    path('gpus', GPUList.as_view(), name='api_gpu_list'),
]