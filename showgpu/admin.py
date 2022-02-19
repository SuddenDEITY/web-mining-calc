from django.contrib import admin
from .models import GPU_Type, Current_Profit, GPU

# Register your models here.
admin.site.register(GPU_Type)
admin.site.register(Current_Profit)
admin.site.register(GPU)