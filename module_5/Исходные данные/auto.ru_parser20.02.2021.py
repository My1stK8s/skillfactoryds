
import requests
import csv
import random
from bs4 import BeautifulSoup
# from pprint import pprint
# from fake_useragent import UserAgent, VERSION
import time
from datetime import datetime
from multiprocessing import Pool  # предоставляет возможность параллельных процессов

AREAS = ['moskva', 'moskovskaya_oblast']
ROOT_URL = 'https://auto.ru/'
ALL_MODELS_URL = 'https://auto.ru/htmlsitemap/mark_model_catalog.html'
CATALOG_URL = 'https://auto.ru/htmlsitemap/mark_model_catalog.html'
LISTING_URL = 'https://auto.ru/-/ajax/desktop/listing/'

# Парсим список наименований моделей sitemap



# def parse_models_list(url, brand):
def parse_models_list(url):
    """
    Парсит названия моделей авто производителя
    # :param url: url
    # :param manufacturer_name: name of the manufacturer
    # :return: list of model names
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sitemap_block = soup.find('div', class_='sitemap')
    all_models_links = sitemap_block.find_all('a')

    # Соберем все названия брендов
    brands_lst = list(set([item['href'].split('/')[-3] for item in all_models_links]))

    models_dict = {}
    for brand_item in brands_lst:
        models_dict[brand_item] = [item['href'].split('/')[-2] for item in all_models_links if
                                   brand_item in item.text.lower()]
    # Сохраним модели только определенного производителя
    # brand_models = [item['href'].split('/')[-2] for item in all_models_links if brand in item.text.lower()]

    #     return brand_models
    return models_dict
models_dct = parse_models_list(CATALOG_URL)


def parse_models_list(url):
    """
    Парсит названия моделей авто производителя
    # :param url: url
    # :param manufacturer_name: name of the manufacturer
    # :return: list of model names
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sitemap_block = soup.find('div', class_='sitemap')
    all_models_links = sitemap_block.find_all('a')

    # Соберем все названия брендов
    brands_lst = list(set([item['href'].split('/')[-3] for item in \
                           all_models_links]))

    models_dict = {}
    for brand_item in brands_lst:
        models_dict[brand_item] = [item['href'].split('/')[-2] for item in \
                                   all_models_links if brand_item in \
                                   item.text.lower()]

    return models_dict


def parse_offer(offer):
    """
    Парсит объявление и создает объект типа словарь с жесткой структурой
    :param offer: dict like object
    :return: fixed structure dictionary object
    """
    item_dict = {}

    try:
        item_dict['bodyType'] = offer['vehicle_info']['configuration']['human_name'].lower()
    except:
        item_dict['bodyType'] = None

    try:
        item_dict['brand'] = offer['vehicle_info']['mark_info']['code']
    except:
        item_dict['brand'] = None

    try:
        item_dict['color_hex'] = offer['color_hex']
    except:
        item_dict['color_hex'] = None

    # try:
    #     item_dict['description'] = offer['description']
    # except:
    #     item_dict['description'] = None

    try:
        item_dict['engineDisplacement'] = offer['vehicle_info']['tech_param']['displacement']
    except:
        item_dict['engineDisplacement'] = None

    try:
        item_dict['enginePower'] = offer['vehicle_info']['tech_param']['power']
    except:
        item_dict['enginePower'] = None

    try:
        if offer['vehicle_info']['equipment'] != {}:
            item_dict['equipment_dict'] = offer['vehicle_info']['equipment']
        else:
            item_dict['equipment_dict'] = None
    except:
        item_dict['equipment_dict'] = None

    # Уже получаем признак model_info ниже
    #     try:
    #         item_dict['model'] = offer['vehicle_info']['model_info']['code']
    #     except:
    #         item_dict['model'] = None

    try:
        item_dict['fuelType'] = offer['vehicle_info']['tech_param']['engine_type']
    except:
        item_dict['fuelType'] = None

    try:
        item_dict['image'] = offer['state']['image_urls'][0]['sizes']['320x240']
    except:
        item_dict['image'] = None

    try:
        item_dict['mileage'] = offer['state']['mileage']
    except:
        item_dict['mileage'] = None

    try:
        item_dict['modelDate'] = offer['vehicle_info']['super_gen']['year_from']
    except:
        item_dict['modelDate'] = None

    try:
        item_dict['model_info'] = offer['vehicle_info']['model_info']
    except:
        item_dict['model_info'] = None

    try:
        item_dict['model_name'] = offer['vehicle_info']['model_info']['code']
    except:
        item_dict['model_name'] = None

    try:
        item_dict['name'] = offer['vehicle_info']['tech_param']['human_name']
    except:
        item_dict['name'] = None

    try:
        item_dict['numberOfDoors'] = offer['vehicle_info']['configuration']['doors_count']
    except:
        item_dict['numberOfDoors'] = None

    item_dict['parsing_unixtime'] = datetime.timestamp(datetime.today())

    try:
        item_dict['priceCurrency'] = offer['price_info']['currency']
    except:
        item_dict['priceCurrency'] = None

    try:
        item_dict['productionDate'] = offer['documents']['year']
    except:
        item_dict['productionDate'] = None

    try:
        item_dict['sell_id'] = int(offer['id'])
    except:
        item_dict['sell_id'] = None

    try:
        item_dict['section'] = offer['section']
    except:
        item_dict['section'] = None

    # saleId
    try:
        item_dict['url_saleid'] = offer['saleId']
    except:
        item_dict['url_saleid'] = None

    try:
        item_dict['super_gen'] = offer['vehicle_info']['tech_param']
    except:
        item_dict['super_gen'] = None

    try:
        part_1 = offer['vehicle_info']['configuration']['body_type']
        part_2 = offer['vehicle_info']['tech_param']['transmission']
        part_3 = str(offer['lk_summary'].split(' ')[0])
        item_dict['vehicleConfiguration'] = f"{part_1} {part_2} {part_3}"
    except:
        item_dict['vehicleConfiguration'] = None

    try:
        item_dict['vehicleTransmission'] = offer['vehicle_info']['tech_param']['transmission']
    except:
        item_dict['vehicleTransmission'] = None

    try:
        item_dict['vendor'] = offer['vehicle_info']['vendor']
    except:
        item_dict['vendor'] = None

    try:
        item_dict['Владельцы'] = round(float(offer['documents']['owners_number']))
    except:
        item_dict['Владельцы'] = None

    if 'pts' in offer['documents']:
        item_dict['ПТС'] = offer['documents']['pts']
    else:
        item_dict['ПТС'] = None

    try:
        item_dict['Привод'] = offer['vehicle_info']['tech_param']['gear_type']
    except:
        item_dict['Привод'] = None

    try:
        item_dict['Руль'] = offer['vehicle_info']['steering_wheel']
    except:
        item_dict['Руль'] = None

    try:
        item_dict['Состояние'] = 'Не требует ремонта' if offer['state']['state_not_beaten'] else 'Битый / не на ходу'
    except:
        item_dict['Состояние'] = None

    try:
        item_dict['Таможня'] = 'Растаможен' if offer['documents']['custom_cleared'] else 'Не растаможен'
    except:
        item_dict['Таможня'] = None

    try:
        item_dict['price'] = offer['price_info']['price']
    except:
        item_dict['price'] = None

    #     try:
    #         item_dict['price_timestamp'] = int(str(offer['price_history'][-1]['create_timestamp'])[:10])
    #     except:
    #         item_dict['price_timestamp'] = None

    try:
        item_dict['auto_class'] = offer['vehicle_info']['configuration']['auto_class']
    except:
        item_dict['auto_class'] = None

    try:
        item_dict['price_segment'] = offer['vehicle_info']['super_gen']['price_segment']
    except:
        item_dict['price_segment'] = None

    try:
        item_dict['seller_type'] = offer['seller_type']
    except:
        item_dict['seller_type'] = None

    return item_dict


def parse_offers_on_page(data):
    """
    Парсит данные с каждого объявления
    :param data: dict like object
    :return: list of offers
    """
    offers_on_page = []
    for offer in data['offers']:
        offers_on_page.append(parse_offer(offer))

    return offers_on_page


# параметры запроса все авто + вся территория
params = {
    "category": "cars",
    "section": "all",
    'damage_group': 'ANY',
    "output_type": "list",
    "top_days": "600",
    "page": 1,
    "page_size": 50,
    "catalog_filter": [{
        "mark": "BMW",
        "model": "1ER"}],
}

headers = """
Host: auto.ru
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://auto.ru/moskovskaya_oblast/cars/bmw/1er/used/?output_type=list&page=2
x-client-app-version: 202009.16.194507
x-page-request-id: 849e1e014809b180dd6369ef515781b9
x-client-date: 1600424297130
x-csrf-token: 9619e4bde43b838e51fb6ec88f45abb5c1375dcf65e03e52
x-requested-with: fetch
content-type: application/json
Origin: https://auto.ru
Content-Length: 127
Connection: keep-alive
Cookie: _csrf_token=9619e4bde43b838e51fb6ec88f45abb5c1375dcf65e03e52; autoru_sid=a%3Ag5f6475822vadaim944uvk3m9k38df0q.ad1235e8bfb82d2e6ccc4e02279be7b8%7C1600419202951.604800.xvQtMDl8gSfu5EwSfkaggw.PAfJWMn3fHWWEPTK-mwweLB582QEQmHtFJ1FSi42Ji8; autoruuid=g5f6475822vadaim944uvk3m9k38df0q.ad1235e8bfb82d2e6ccc4e02279be7b8; suid=eb6987df5285415441449e94a1b41c80.d49f33fd60e906b91504804f403170d7; from_lifetime=1600424294237; from=direct; yuidcs=1; X-Vertis-DC=myt; yuidlt=1; yandexuid=4092999901600419204; counter_ga_all7=2; _ym_uid=1600419208166105885; _ym_d=1600424294; _ym_isad=2; crookie=tA8s7HCAVpgyzbZkV3K3hwGTs1rRKZRrq7yjQ6jXpUo/h4XStsR35QSw2azg6f2daVQSwtDViKNra0er/NkQPZYfcqM=; cmtchd=MTYwMDQxOTIwODYyMA==; _ga=GA1.2.464157848.1600422869; _gid=GA1.2.61052704.1600422869; _ym_wasSynced=%7B%22time%22%3A1600422869584%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D; gdpr=0; _ym_visorc_22753222=b; cycada=fGsHIePtGydQvy2cOf9SC3d5qV8+cFZcW+Z4bWJWuno=; _ym_visorc_148422=w; _ym_visorc_148383=w"""
headers = headers.strip().split('\n')

dict_headers = {}
for header in headers:
    key, value = header.split(': ')
    dict_headers[key] = value


def collect_car_brand_ads(brand, model, section):
    """
    Основная функция парсинга всех объявлений по продаже
    моделей авто, переданного в параметре бренда.
    :param brand: string
    :return: list of dicts
    """
    # brand_offers = []

    global response
    params['catalog_filter'][0]['mark'] = brand.upper()

    offers_by_model = []
    params['catalog_filter'][0]['model'] = model.upper()
    params['section'] = section
    params['page'] = 1

    try:
        response = requests.post(LISTING_URL, json=params,
                                 headers=dict_headers)
    except:
        print(f"Requests: raised exception by {brand} {model}")

    try:
        data = response.json()
    except:
        print(f"Raise error to read JSON obj by {brand} {model}.")
        return

    if 'offers' not in data or len(data['offers']) == 0:  # объявлений нет
        print(f"{brand.upper()} {model.upper()} {section}: no offers.")
        return

    total_page_count = int(data['pagination']['total_page_count'])
    # print(f"TOTAL PAGE COUNT: {total_page_count} шт.")
    #     if total_page_count <= 1:  # !!!!!!!!!!!!!!!!!!!!!!
    #         if len(data['offers']) == 0:  # Удалить строчку, так как она есть выше
    #             return
    #         offers_by_model += parse_offers_on_page(data)
    #     else:
    # Cтраниц 1 и больше
    for page in range(1, total_page_count + 1):
        # print(f".", end='')
        params['page'] = page
        response = requests.post(LISTING_URL, json=params,
                                 headers=dict_headers)
        data = response.json()

        if 'offers' not in data or len(data['offers']) == 0:  # дошли до конца списка
            break
        offers_by_model += parse_offers_on_page(data)
        time.sleep(random.randint(1, 3))

    # print(f"{brand} {model}: collected: {len(offers_by_model)} offers.")
    # brand_offers += offers_by_model

    print(f"{brand.upper()} {model.upper()} {section}: collected {len(offers_by_model)} offers.")

    return offers_by_model

###### ПАРСИТЬ ГРУППАМИ ИНАЧЕ ВЫДАЕТ  ОГШИБКУ########
def parse_models_dict():
    """
    Парсит наименования моделей по брендам.
    :return: a dict
    """
    models_dict = parse_models_list(CATALOG_URL)

     european_brands = ['SKODA', 'PORSCHE', 'CITROEN', 'JAGUAR', 'RENAULT',
                        'VOLKSWAGEN', 'VOLVO', 'MERCEDES', 'OPEL', 'BMW',
                        'FIAT', 'MINI', 'AUDI', 'PEUGEOT']

     japanese_brands = ['SUZUKI', 'HONDA', 'INFINITI', 'LEXUS', 'TOYOTA', 'SUBARU',
                        'NISSAN', 'MITSUBISHI', 'MAZDA']

    # selected_brands = european_brands + japanese_brands
    selected_brands = japanese_brands+european_brands
    # переведем строки в нижний регистр
    selected_brands = list(map(str.lower, selected_brands))

    # Удалим из словаря те бренды, которых нет в selected_brands
    items_to_delete = list(set(models_dict.keys()) - set(selected_brands))

    for item in items_to_delete:
        _ = models_dict.pop(item)

    return models_dict


# def write_csv(data_list):
#     """
#     Получает список словарей и записывает
#     в csv-файл
#     :param data_list: a list of dicts
#     """
#     with open('cars_prices_multiprocessing_08_11_2020.csv', 'a') as csv_file:
#         fieldnames = data_list[0].keys()
#         writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
#
#         writer.writeheader()
#         for item_dict in data_list:
#             writer.writerow(item_dict)
# Немного переписанныя функция для устранения возникающего исключения с декодированием символов типа '/u2705'
def write_csv(data_list):
    """
    Получает список словарей и записывает
    в csv-файл
    :param data_list: a list of dicts
    """
    with open('TOYOTA.csv', 'a', encoding='utf8') as csv_file:
        fieldnames = data_list[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item_dict in data_list:
            try:
                writer.writerow(item_dict)
            except UnicodeEncodeError:
                # выведем на экран те данные, которые не смогли пройти декодирование
                print(f"Raise exception UnicodeEncodeError. \nData: {item_dict}")

def parse_model_offers(data):
    """
    Парсит все объявления по переданному
    бренду и модели авто. Записывает в csv-файлю.
    :param data: tuple of 2 strings
    :return: nothing
    """
    brand, model = data
    sections = ['new', 'used']
    for section in sections:
        data = collect_car_brand_ads(brand, model, section)
        if data:
            write_csv(data)


def get_cars_list():
    """
    Создает и возращает список кортежей (бренд, модель)
    :return: list of tuples
    """
    data_dict = parse_models_dict()
    tmp_lst = []

    for brand, models in data_dict.items():
        tmp_lst += [(brand, model) for model in models]

    return tmp_lst


if __name__ == '__main__':

    """
    Основная функция многопоточного парсера.
    """
    start = datetime.now()
    model_brand_tuples_lst = get_cars_list()

    with Pool(20) as p:
        p.map(parse_model_offers, model_brand_tuples_lst)

    end = datetime.now()
    delta = end - start
    print(f"Total time: {round((end - start).seconds / 60)} mins.")
