import json
import requests
from random import randint
food_choice = input('Pleae enter your dinner choice: ')

url = f'https://api.punkapi.com/v2/beers?food={food_choice}'

url_request = requests.get(url)

# loads() and get() and .text
data = json.loads(url_request.text)

# print(data[0]['name'], data[0]['tagline'], data[0][])

beer_list = []

for beer in data:
    name = beer['name']
    tagline = beer['tagline']
    abv = beer['abv']

    beer_item = {
        'name': name,
        'tagline': tagline,
        'abv': abv
    }

    beer_list.append(beer_item)

value = randint(0,len(beer_list))

try_this = beer_list[value]

try_name = try_this['name']
try_tagline = try_this['tagline']
try_abv = try_this['abv']

print(f'You should try {try_name}, {try_tagline}, {try_abv}, %')



