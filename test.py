from framework import *


dir = "n"
payload = {"direction": dir}
exits = [dir]

while dir in exits:

    data = move(payload)
    print('\nwe are moving in this direction: ', exits, '\n')

    # print('data inside the while loop', data)

    if not data:
        print('no data available peaaace')
        break

    if len(data['errors']) > 0:
        print('errors', data['errors'])
        print('\a')
        break

    items = data['items']

    room_obj = {
        "room_id": data['room_id'],
        "title": data['title'],
        "items": data['items'],
        "exits": data['exits'],
        "cooldown": data['cooldown'],
        "errors": data['errors'],
        'messages': data['messages'],
    }

    print(room_obj)

    if data['room_id'] == 467:
        print('i think we found the pirates cove to change name?!!!!')
        print('\a')
        break

    if data['room_id'] == 20:
        break

        #     break

    if "ishing" in room_obj["title"]:
        print('i think we found the wishing well?')
        print(room_obj["title"])
        print(room_obj["room_id"])
        print('\a')
        break

    # if len(items) > 0:
    #     print('we found a items!!!!')
    #     print('items', items)
    #     time.sleep(16)
    #     for item in items:
    #         data = get_item({"name": f"{item}"})
    #         print('message: ', data['messages'])

    print('begin cooldown time: ', room_obj['cooldown'])
    time.sleep(room_obj['cooldown'])

print('\a')
