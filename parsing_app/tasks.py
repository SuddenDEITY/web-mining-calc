from celery import shared_task
from showgpu.models import GPU_Type, Current_Profit
from django.utils import timezone
from .shops_parsers import initialize_parsing
import json
import requests
from bs4 import BeautifulSoup

@shared_task(bind=True)
def update_gpu_type_profit(self):
    '''Updating GPU_Type objects with new data, if something fails startover in 60 secs'''
    try:
        d = {}
        current_profit = Current_Profit.objects.first()
        gpu_types = GPU_Type.objects.all()
        for el in gpu_types:
            eth_profit = float(current_profit.eth_daily_profit_per_100mhs * el.eth / 100) # calculating eth profit for individula gpu_type
            ton_profit = float(current_profit.ton_daily_profit_per_1ghs * el.ton / 1000) # calculating ton profit for individula gpu_type
            d['eth'] = eth_profit
            d['ton'] = ton_profit
            el.primary_token = max(d, key=d.get) # getting primary_token (the most profitablle coin to mine)
            el.day_profit = d[el.primary_token]
            el.month_profit = el.day_profit * 30
            
        GPU_Type.objects.bulk_update(gpu_types, ['primary_token','day_profit','month_profit'])
        print('gpu_types updated')
        initialize_parsing.delay()
    except:
        print('update gpu_types failed,retry in 60 seconds')
        self.retry(countdown=60)

@shared_task(bind=True)
def check_profit(self):
    '''Updating Current_Profit with new data, if parsing fails retrying in 60 secs'''
    try:
        current_profit = Current_Profit.objects.first()
        current_profit.usd_price, current_profit.eur_price = usd_eur_price() 
        current_profit.eth_daily_profit_per_100mhs = get_eth_profit() * current_profit.usd_price # getting eth profit in usd
        current_profit.ton_daily_profit_per_1ghs = get_ton_profit() * current_profit.usd_price # getting ton profit in usd
        current_profit.updated_at = timezone.now()
        current_profit.save()
        update_gpu_type_profit.delay()
    except:
        print('currentprofit failed,retry in 60 seconds')
        self.retry(countdown=60)



def get_eth_profit():
    '''Parse and calculate current profitability for eth mining'''
    r = requests.get(f'https://whattomine.com/coins/151-eth-ethash/history?cost=0.07&fee=0.0&format=json&hr=100&p=250', timeout=(10, 10))
    data = json.loads(r.text)
    daily_profit = float(data[3]['data'][0]['y'])
    return daily_profit

def get_ton_profit():
    '''Parse and calculate current profitability for ton mining'''
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'}
    r = requests.get(f'https://next.ton-pool.com/stats')
    data = json.loads(r.text)
    daily_profit = float(data['income']['last_24h'] / 10**9) # division by 10**9 to get profit in coins
    r = requests.get('https://price-api.crypto.com/price/v1/exchange/toncoin', headers=headers)
    data = json.loads(r.text)
    toncoin_usd_price = float(data['fiat']['usd'])
    kw_spent_for_24h = 75 / 1000 * 24 # 75w devide by 1000 and multiply by 24 to get how much kw spent in 24h
    electricity_consumption = kw_spent_for_24h * 0.07 # 0.07 - price for kw/h in usd
    daily_profit *= toncoin_usd_price # getting daily_profit in usd
    return daily_profit - electricity_consumption

def usd_eur_price():
    '''Parse usd and eur price from cbr.ru'''
    r = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp')
    soup = BeautifulSoup(r.text,'xml')
    dollar_tag = soup.find(attrs={"ID" : "R01235"})
    dollar_price = dollar_tag.select('Value')[0].get_text().replace(',', '.')
    eur_tag = soup.find(attrs={"ID" : "R01239"})
    eur_price = eur_tag.select('Value')[0].get_text().replace(',', '.')
    return float(dollar_price),float(eur_price)