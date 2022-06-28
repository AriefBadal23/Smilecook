# import requests

# response = requests.get('https://api.stackexchange.com/2.3/articles?order=desc&sort=activity&site=stackoverflow')

# print(response.json())

import json

person_list = []

# Context manager(best practice)
# opening file and store in variable
with open('data.json') as json_file:
    # load data in variable
    data = json.load(json_file)
    for item in data:
        firstname = item['first_name']
        lastname = item['first_name']
        email = item['email']

        person = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        }

        person_list.append(person)


print(person_list)



