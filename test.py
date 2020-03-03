from framework import *


dir = "s"
payload = {"direction": dir}
exits = [dir]

while dir in exits:

    data = move(payload)

    print('data inside the loop', data)

    if not data:
        print('no data available peaaace')
        break

    if len(data['errors']) > 0:
        print('errors', data['errors'])
        break

    if data['room_id'] == 0:
        break

    items = data['items']
    print(data['exits'])

    if len(items) > 0:
        print('we found a items!!!!')
        print('items', items)
        time.sleep(16)
        for item in items:
            data = get_item({"name": f"{item}"})
            print('data for items', data)

    time.sleep(16)
