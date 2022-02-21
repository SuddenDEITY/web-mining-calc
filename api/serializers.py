from rest_framework import serializers
from showgpu.models import GPU

class GPUSerializer(serializers.ModelSerializer):
    gpu_type = serializers.CharField(source='gpu_type.code')
    eth_hashrate = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.eth')
    ton_hashrate = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.ton')
    day_profit = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.day_profit')
    month_profit = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.month_profit')
    day_profit_dual = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.day_profit_dual')
    month_profit_dual = serializers.DecimalField(max_digits=10, decimal_places=1,source='gpu_type.month_profit_dual')
    class Meta:
        model = GPU
        queryset = GPU.objects.select_related('gpu_type').all().order_by('payback_dual')
        
        fields = ('id','link','shop','title', 'price', 'payback', 'payback_dual', 'gpu_type', 'eth_hashrate', 'ton_hashrate', 'day_profit', 'month_profit', 'day_profit_dual', 'month_profit_dual')