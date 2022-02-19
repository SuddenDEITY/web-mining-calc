from django.urls import path
from .views import GPU_Type_List

urlpatterns = [
    path('', GPU_Type_List.as_view(), name='gpu_list'),
]

