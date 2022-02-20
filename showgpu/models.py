from django.db import models

class Current_Profit(models.Model):
    ton_daily_profit_per_1ghs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eth_daily_profit_per_100mhs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usd_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    eur_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    updated_at = models.DateTimeField(null=True,blank=True)
    
    def __str__(self) -> str:
        return self.updated_at.strftime("%d-%m %H:%M:%S")

    class Meta:
        verbose_name = 'Current profit'
        verbose_name_plural = 'Current profit'

class GPU_Type(models.Model):
    name = models.CharField(max_length=30)
    eth = models.DecimalField(max_digits=10, decimal_places=1, default=0) #hashrate on eth
    ton = models.DecimalField(max_digits=10, decimal_places=1, default=0) #hashrate on ton
    day_profit = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
    month_profit = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
    day_profit_dual = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
    month_profit_dual = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
    dual_efficiency = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=30)
    primary_token = models.CharField(max_length=20, blank=True, default='eth')
    code = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Type of GPU'
        verbose_name_plural = 'Types of GPU'

    def save(self, *args, **kwargs):
        self.code = self.name.lower().strip().replace(' ','') # adding code when saving object
        super(GPU_Type, self).save(*args, **kwargs)

class GPU(models.Model):
        shop = models.CharField(max_length=30,null=True,blank=True)
        title = models.CharField(max_length=200,null=True,blank=True)
        link = models.TextField()
        payback = models.IntegerField(null=True, blank=True)
        payback_dual = models.IntegerField(null=True, blank=True)
        gpu_type = models.ForeignKey(GPU_Type, on_delete=models.CASCADE, related_name='gpu_type', null=True)
        price = models.IntegerField(null=True, blank=True)

        def __str__(self) -> str:
            return self.title
        
        class Meta:
            verbose_name = "GPU"
            verbose_name_plural = "GPU's"
    