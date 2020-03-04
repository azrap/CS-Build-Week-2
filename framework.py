import time
import requests
import json


Token = "a7af7d4d70b5e0f6d5032a265a84d496ac3b3d30"

url = "https://lambda-treasure-hunt.herokuapp.com/api"


headers = {'Authorization': f'Token {Token}'}


def init():
    r = requests.get(
        f'{url}/adv/init/', headers=headers)

    data = r.json()
    print(data)
    print(data["items"])
    if len(data['errors']) > 0:
        print(data)
        return False
    return data


def move(payload):
    r_move = requests.post(
        f'{url}/adv/move/', data=json.dumps(payload), headers=headers)
    data = r_move.json()
    # print('data inside the move', data)
    if len(data['errors']) > 0:
        print('move error', data)
        return False
    return data


def get_item(item):
    r = requests.post(f'{url}/adv/take',
                      data=json.dumps(item), headers=headers)
    data = r.json()
    if len(data['errors']) > 0:
        print('get_item error', data['errors'])
        return False
    return data
