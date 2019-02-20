import requests
import json
from data import data_from_dict
import os
import time

URI = 'https://www.cian.ru/cian-api/mobile-site/v2/search-offers/'

os.remove('output.txt')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

data = {'region': {'type': 'terms',
                   'value': [1]
                   },
        '_type': 'commercialsale',
        'category': {'type': 'terms', 'value':['commercialLandSale']},
        # 'office_type': {'type': 'terms', 'value': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]},
        'engine_version': {'type': 'term', 'value': 2},
        'page': {'type': 'term',
                 'value': 1
                 }
        }

response = requests.post(
    URI, headers=headers, data=json.dumps(data))

with open('output.txt', 'a+') as text_file:
    print(response.text, file=text_file)

result = data_from_dict(response.json())

print(result.data.offers_serialized)

pages = result.data.aggregated_count // len(result.data.offers_serialized) + 1

for x in range(52, pages):
    data['page']['value'] = x
    response = requests.post(
        URI, headers=headers, data=json.dumps(data))
    with open('output.txt', 'a+') as text_file:
        print(response.text, file=text_file)
    result = data_from_dict(response.json())
    print(result.data.offers_serialized, x)
    time.sleep(3)
