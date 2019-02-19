import requests
import json
from data import data_from_dict


headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
}

data = {'region': {'type': 'terms',
                   'value': [4704]
                   },
        '_type': 'commercialsale',
        'office_type': {'type': 'terms', 'value': [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12]},
        'engine_version': {'type': 'term', 'value': 2},
        'page': {'type': 'term',
                 'value': 2
                 }
        }

response = requests.post(
    'https://volgograd.cian.ru/cian-api/mobile-site/v2/search-offers/', headers=headers, data=json.dumps(data))

with open("output.txt", "w") as text_file:
    print(response.text, file=text_file)

result = data_from_dict(response.json())

print(result.data.offers_serialized)
