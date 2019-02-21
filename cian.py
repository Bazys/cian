import requests
import json
from data import data_from_dict
import os
import time

URI = 'https://api.cian.ru/search-offers/v2/search-offers-desktop/'
file_path = 'output.json'

if os.path.exists(file_path):
    os.remove(file_path)


headers = {
    'Accept': 'application/json',
    'Content-Type': 'text/plain;charset=UTF-8',
}
data = {
    "jsonQuery": {
        "region":
        {"type": "terms",
         "value": [4704]
         },
        "_type": "commercialsale",
        # 'category': {'type': 'terms', 'value': ['commercialLandSale']},
        # 'category': {'type': 'terms', 'value': ['commercialLandSale', 'buildingSale', 'officeSale', 'freeAppointmentObjectSale', 'shoppingAreaSale']},
        "office_type": {
            "type": "terms",
            "value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        "engine_version": {
            "type": "term",
            "value": 2
        },
        "page": {
            "type": "term",
            "value": 1
        }
    }
}

response = requests.post(
    URI, headers=headers, data=json.dumps(data))

with open(file_path, 'a+', encoding='utf-8') as text_file:
    print(response.text.encode().decode('unicode-escape'), file=text_file)
    # print(response.text, file=text_file)

result = data_from_dict(response.json())

print(result.data.offers_serialized)

pages = result.data.aggregated_count // len(result.data.offers_serialized) + 1
if pages > 60:
    pages = 60

for x in range(2, pages):
    data['jsonQuery']['page']['value'] = x
    response = requests.post(
        URI, headers=headers, data=json.dumps(data))
    with open(file_path, 'a+', encoding='utf-8') as text_file:
        print(response.text.encode().decode('unicode-escape'), file=text_file)
        # print(response.text, file=text_file)
    result = data_from_dict(response.json())
    print(result.data.offers_serialized, x)
    time.sleep(3)
