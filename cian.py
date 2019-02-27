import requests
import json
# from data import data_from_dict
import os
import time
import pymongo
from pymongo import MongoClient


def stripNone(data):
    if isinstance(data, dict):
        return {k: stripNone(v) for k, v in data.items() if k is not None and v is not None}
    elif isinstance(data, list):
        return [stripNone(item) for item in data if item is not None]
    elif isinstance(data, tuple):
        return tuple(stripNone(item) for item in data if item is not None)
    elif isinstance(data, set):
        return {stripNone(item) for item in data if item is not None}
    else:
        return data


# URI = 'https://api.cian.ru/search-offers/v2/search-offers-desktop/'
URI = 'https://www.cian.ru/cian-api/mobile-site/v2/search-offers/'
file_path = 'output.json'

if os.path.exists(file_path):
    os.remove(file_path)


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'DNT': '1',
    'Origin': 'null'
}
data = {
    "region": {
        "type": "terms",
        "value": [4704]
    },
    "publish_period": {
        "type": "term",
        "value": 600
    },
    "_type": "commercialsale",
    'category': {
        'type': 'terms',
        'value': [
            'commercialLandSale',
            # 'garageSale',
            # 'businessSale',
            'buildingSale',
            'officeSale',
            'freeAppointmentObjectSale',
            'shoppingAreaSale',
            # 'industrySale'
        ]},
    # "office_type": {
    #     "type": "terms",
    #     "value": [1,  # Офис
    #               2,  # Торговая площадь
    #               3,  # Склад
    #               4,  # ПСН
    #               5,  # Общепит
    #               6,  # Гараж
    #               7,  # Производство
    #               8,  # Автосервис
    #               9,  # Готовый бизнес
    #               10,  # Здание
    #               11,  # Бытовые услуги
    #               12  # Коммерческая земля
    #               ]
    # },
    "engine_version": {
        "type": "term",
        "value": 2
    },
    "page": {
        "type": "term",
        "value": 1
    }
}
client = MongoClient('mongodb://localhost:27017/')
db = client.cian
collection = db.offers
collection.create_index([('id', pymongo.ASCENDING)], unique=True)

response = requests.post(URI, headers=headers, data=json.dumps(data))

# with open(file_path, 'a+', encoding='utf-8') as text_file:
#     print(response.text.encode().decode('unicode-escape'), file=text_file)

# result = data_from_dict(response.json()).data
result = response.json()['data']

print(result['aggregatedCount'])

if len(result['offersSerialized']) > 0:
    for offer in result['offersSerialized']:
        filtered_offer = stripNone(offer)
        collection.find_one_and_replace(
            {"id": offer['id']}, filtered_offer, upsert=True)


pages = result['aggregatedCount'] // len(result['offersSerialized']) + 2

if pages > 60:
    pages = 60

if pages > 2:
    for x in range(2, pages):
        data['page']['value'] = x
        # data['jsonQuery']['page']['value'] = x
        response = requests.post(URI, headers=headers, data=json.dumps(data))
        result = response.json()['data']
        # result = data_from_dict(response.json()).data
        for offer in result['offersSerialized']:
            filtered_offer = stripNone(offer)
            collection.find_one_and_replace(
                {"id": offer['id']}, filtered_offer, upsert=True)
        print('Page:', x)
        time.sleep(2)
