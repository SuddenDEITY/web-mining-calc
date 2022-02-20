from django.shortcuts import render,redirect
from .models import GPU_Type, Current_Profit
from django.views import View


class GPU_Type_List(View):
    def get(self, request):
        current_profit = Current_Profit.objects.first()
        electricity = round(0.07 * float(current_profit.usd_price),2) # calculating kw/h price in rub      
        last_update = current_profit.updated_at.strftime("%H:%M:%S") # formating updated_at to friendly view
        gpu_list = GPU_Type.objects.all()
        if len(gpu_list) > 0: # if user send request in timing when db already removed all objects, but not yet created, redirects user to itself
            return render(request, 'showgpu/gpu_type_list.html', {'gpu_type_list':gpu_list, 'last_update': last_update, 'current_profit':current_profit, 'electricity':electricity})
        else:
            return redirect('gpu_list')