from django.shortcuts import render,redirect
from .models import Current_Profit, GPU
from django.views import View


def filtration(request):
    '''Check if filter params specified, filter and return query, if not, returns default query'''
    d = {}
    if len(request.GET) != 0:
        for k,v in request.GET.items():
            if len(v.split('-')) > 1:
                d[k + '__in'] = v.split('-')
            else:
                d[k] = v
        try: # if filter doesnt exist return default query
            return GPU.objects.all().select_related('gpu_type').filter(**d).order_by('payback_dual')
        except:
            return GPU.objects.all().select_related('gpu_type').order_by('payback_dual')

    return GPU.objects.all().select_related('gpu_type').order_by('payback_dual')



class GPU_Type_List(View):
    def get(self, request):
        current_profit = Current_Profit.objects.first()
        electricity = round(0.07 * float(current_profit.usd_price),2) # calculating kw/h price in rub      
        last_update = current_profit.updated_at.strftime("%H:%M:%S") # formating updated_at to friendly view
        gpu_list = filtration(request)

        if len(gpu_list) > 0: # if user send request in timing when db already removed all objects, but not yet created, redirects user to this view
            return render(request, 'showgpu/gpu_list.html', {'gpulist':gpu_list, 'last_update': last_update, 'current_profit':current_profit, 'electricity':electricity})
        else:
            return redirect('gpu_list')