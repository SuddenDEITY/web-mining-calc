from playwright.sync_api import sync_playwright 
from playwright_stealth import stealth_sync
from showgpu.models import GPU, GPU_Type,Current_Profit
from celery import shared_task
from django.utils import timezone
import json
from django.core.cache import cache

class Data():
    current_profit = None
    gpu_types = None
    models = None
    eur_price = None
    cu_response_list = []
    result_data = []
    bulk_data = []


# Main function
@shared_task(bind=True)
def initialize_parsing(self):
    '''Save parsed objects to db with bulk_create method and update current_profit "updated_at" time'''
    try:
        erase_everything()
        get_current_profit()
        get_gpu_types()
        get_models()
        get_cu_gpus()
        get_dns_gpus()
        GPU.objects.all().delete()
        GPU.objects.bulk_create(Data.bulk_data)
        cp = Data.current_profit
        cp.updated_at = timezone.now()
        cache.clear()
        cache.set("gpu_list", GPU.objects.all().select_related('gpu_type').order_by('payback_dual'), None)
        cache.set("current_profit", cp, None)
        cp.save()
        print('updated')
    except:
        print('parsing failed,retry in 60 seconds')
        self.retry(countdown=60)

# General functions

def get_current_profit():
    current_profit = Current_Profit.objects.first()
    Data.current_profit = current_profit

def get_gpu_types():
    '''Get all gpu_type objects and put them in Data class variable'''
    gpu_types = GPU_Type.objects.all()
    Data.gpu_types = gpu_types

def get_models():
    '''Get all gpu_type objects codes, put them in a list and sort it'''
    models = Data.gpu_types
    models = [el.code for el in models]
    models = sorted(models,key=lambda s: len(s))
    models.reverse()
    Data.models = models

def get_model(name):
    '''Iterates list with sorted codes and check if current gpu code equal'''
    name = name.lower().replace(' ','').strip()
    for el in Data.models:
        if el in name:
            return el
    return None

def erase_everything():
    '''Clear all Data class data'''
    Data.models = None
    Data.gpu_types = None
    Data.result_data = []
    Data.bulk_data = []

# DNS shop functions

def get_dns_gpus():
        '''Initialize browser, call parser functions,transform raw objects to normal'''
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(30000) 
            stealth_sync(page)
            last_page = dns_init_and_take_first_page(page)
            if last_page > 1:
                for _ in range(last_page-1):
                    page.query_selector_all('.pagination-widget__page')[-2].click()
                    page.wait_for_timeout(1000)
                    dns_add_result(page)
            browser.close()

        for el in Data.result_data:
            try:
                gpu_type_object_id = Data.gpu_types.get(code=el[3]).id
                payback = el[2] / float(Data.gpu_types.get(code=el[3]).day_profit)
                payback_dual = el[2] / float(Data.gpu_types.get(code=el[3]).day_profit_dual)
                Data.bulk_data.append(GPU(shop='DNS',title=el[0],link=el[1],price=el[2],gpu_type_id=gpu_type_object_id,payback=payback,payback_dual=payback_dual))
            except:
                print(el)
        Data.result_data = []
        print('dns parsing done') 

def dns_init_and_take_first_page(page):
    '''Going to first page, parsing gpu data and pagination info(last_page)'''
    page.goto("https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mx]=2ff-2fi-udtfd-2fh-dbbc-d8xw?p=1")
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)
    dns_add_result(page)   
    pagination = page.query_selector_all('.pagination-widget__page')
    last_page = pagination[-3].inner_text()
    return int(last_page)

def dns_add_result(page):
    '''Parsing current page, calculate some values of gpu, and append raw gpu "object" to list'''
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(1000)
    products = page.query_selector_all('.catalog-product')
    for el in products:
        link = 'https://www.dns-shop.ru/' + el.query_selector('.catalog-product__name').get_attribute('href')
        name = el.query_selector('.catalog-product__name').inner_text().split('[')[0].replace('Видеокарта', '')
        if el.query_selector('.product-buy__sub_active'):
            default_price = int(el.query_selector('.product-buy__price').inner_text().split('₽')[0].replace(' ', ''))
            discount = int(el.query_selector('.product-buy__sub_active').inner_text().replace('доп. скидка ', '').replace(' ₽', '').replace(' ', ''))
            price = default_price - discount
        else:
            price = int(el.query_selector('.product-buy__price').inner_text().split('₽')[0].replace(' ', ''))
        model = get_model(name)
        Data.result_data.append([name,link,price,model])

# CU functions

def get_cu_gpus():
        '''Initialize browser, call parser functions,transform raw objects to normal'''
        with sync_playwright() as p:
            browser = p.firefox.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(30000) 
            stealth_sync(page)
            last_page = cu_init_and_take_first_page(page)
            if last_page > 1:
                for _ in range(last_page-1):
                    page.query_selector('#main-content > div > div.flex.flex-nowrap.flex-col.md\:flex-row.md\:flex-wrap.justify-center.items-center.md\:justify-end.mx-auto.bg-blue-400.rounded-cu-10.p-2.md\:rounded-tl-none > ul > li.Pagination__naviButton.false > button').click()
                    cu_parse_all_pages(page)
            browser.close()

        for el in Data.result_data:
            try:
                gpu_type_object_id = Data.gpu_types.get(code=el[3]).id
                payback = el[2] / float(Data.gpu_types.get(code=el[3]).day_profit)
                payback_dual = el[2] / float(Data.gpu_types.get(code=el[3]).day_profit_dual)
                Data.bulk_data.append(GPU(shop='CU',title=el[0],link=el[1],price=el[2],gpu_type_id=gpu_type_object_id,payback=payback,payback_dual=payback_dual))
            except:
                print(el)
        Data.result_data = []
        print('cu parsing done')
        
def cu_log_request(intercepted_request):
    '''Put all requests in list'''
    if 'https://search.computeruniverse.net/search' in intercepted_request.url:
        Data.cu_response_list.append(intercepted_request)

def cu_remove_shit(data):
    '''Removing not necessary words from object name'''
    return data.replace('видеокарта','').replace('Enthusiast','').replace('OC','').replace('High End','').replace('16GB', '')\
                .replace('8.0 GB', '').replace('16.0 GB', '').replace('24 GB', '').replace('10GB', '').replace('12GB', '').replace('8GB', '')\
                .replace('12 GB', '').replace('6GB', '').replace('6.0 GB', '').replace('20GB', '').strip()

def cu_add_result(data):
    '''Parsing data, calculate some values of gpu, and append raw gpu "object" to list'''
    for el in data['results'][0]['hits']:
        name = cu_remove_shit(el['name'])
        price = float(el['price_ag'])
        delivery = price * 0.07
        fee = 0 if price < 200 else (price-200)*0.15
        price_in_rub = (price + delivery + fee) * float(Data.current_profit.eur_price)
        url = 'https://www.computeruniverse.net/'+el['url']
        gpu_type = get_model(name)
        Data.result_data.append([name,url,price_in_rub,gpu_type])
 
def cu_parse_all_pages(page):
    '''Iterate all available pages and get data from them'''
    page.on("response", cu_log_request)
    page.wait_for_load_state("domcontentloaded")
    page.query_selector('//*[@id="main-content"]/div/div[1]/div[2]/div[1]/div[2]/select').select_option('60')
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)
    page_data = Data.cu_response_list[-1].body().decode('utf8')
    data = json.loads(page_data)
    cu_add_result(data)

def cu_init_and_take_first_page(page):
    '''Going to first page, parsing gpu data and pagination info(last_page)'''
    page.on("response", cu_log_request)
    page.goto("https://www.computeruniverse.net/ru/c/apparatnoe-obespechenie-i-komponenty/videokarty-pci-express?range%5Bfacets.Speicher%2528VRAM%2529.valuesDisplayOrder%5D%5Bmin%5D=14&toggle%5Bdeliverydatenow%5D=true?page=1")
    page.wait_for_load_state("domcontentloaded")
    page.query_selector('//*[@id="main-content"]/div/div[1]/div[2]/div[1]/div[2]/select').select_option('60')
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_timeout(3000)
    page_data = Data.cu_response_list[-1].body().decode('utf8')
    data = json.loads(page_data)
    cu_add_result(data)
    
    pagination = page.query_selector_all('.Pagination__item')
    last_page = max([el.inner_text() for el in pagination])
    return int(last_page)