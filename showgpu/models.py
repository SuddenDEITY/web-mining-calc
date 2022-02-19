from django.db import models

# Create your models here.

class GPU_Type(models.Model):
    name = models.CharField(max_length=30)
    eth = models.DecimalField(max_digits=10, decimal_places=1, default=0) #hashrate on eth
    ton = models.DecimalField(max_digits=10, decimal_places=1, default=0) #hashrate on ton
    day_profit = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
    month_profit = models.DecimalField(max_digits=10,decimal_places=2, blank=True, default=0)
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