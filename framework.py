import time
import requests
import json


url = "https://lambda-treasure-hunt.herokuapp.com/api"


def init():
    r = requests.get(
        f'{url}/adv/init/', headers=headers)

    data = r.json()
    print(data)
    print(data['items'])
    if len(data['errors']) > 0:
        print(data)
        return False
    return data


payload = {"direction": "e"}
exits = ["e"]


def move(payload):
    r_move = requests.post(
        f'{url}/adv/move/', data=json.dumps(payload), headers=headers)
    data = r_move.json()
    print('data inside the move', data)
    if len(data['errors']) > 0:
        print(data)
        return False
    return data


while "e" in exits:
    data = move(payload)
    print('data inside the loop', data)
    if not data:
        break

    # if len(data['errors']) > 0:
    #     print('errors', data)
    #     break
    # print(data['items'])
    # exits = data['exits']
    time.sleep(20)
