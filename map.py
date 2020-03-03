import json
import requests
from time import sleep
from decouple import config


url = 'https://lambda-treasure-hunt.herokuapp.com/api/adv'
TOKEN = config('token')
headers = {'Authorization': 'Token ' + TOKEN}

# Reverse directions
reverse_dir = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# Keep track of reverse path for backtracking
reverse_path = []

# Collect room data
rooms = {}

# Dictionary to iterate through exits
exits = {}

# Keep track of graph
graph = {}

# Movement payload for post request
payload = {
    'n': {"direction": "n"},
    's': {"direction": "s"},
    'e': {"direction": "e"},
    'w': {"direction": "w"}
}

# While rooms visited is less than total rooms...
while len(rooms) < 500-1:
    # Keep track of previous room
    prev_room = None
    # Inspect current room
    r = requests.get(url=url + '/init', headers=headers)
    sleep(5)
    print('new room:', r.json())
    current_room = r.json()['room_id']
    print('current_room:', current_room)

    # If room hasn't been visited...
    if current_room not in rooms:
        rooms[current_room] = {
            'title': r.json()['title'],
            'description': r.json()['description'],
            'coordinates': r.json()['coordinates'],
            'exits': r.json()['exits'],
            'cooldown': r.json()['cooldown'],
            'errors': r.json()['errors'],
            'messages': r.json()['messages']
        }

        # Add exits for current room to rooms
        exits[current_room] = r.json()['exits']
        print('List of exits for the room', exits[current_room])
        # Grab last direction traveled
        if prev_room is not None:
            print('prev_room:', prev_room)
            last_dir = reverse_path[-1]
            # Remove last exit from exits
            exits[current_room].remove(last_dir)
            print('Exits after removing last direction:', exits[current_room])
            # Initialize graph room
            graph[current_room] = {'n': '?', 's': '?', 'e': '?', 'w': '?'}
            # Update graph for previous room
            if graph[prev_room][last_dir] == '?':
                graph[prev_room][last_dir] = current_room
                graph[current_room][reverse_dir[last_dir]] = prev_room
                print('Graph:', graph)

        # While there's no more rooms to explore...
        while len(exits[current_room]) < 1:
            # Pop last direction in reverse_path
            reverse = reverse_path.pop()
            # Move in reverse direction
            requests.post(url + "/move", headers=headers,
                          data=payload[reverse])
            print('backtracking...')

    # Travel in first available exit direction in room
    exit_dir = exits[current_room].pop(0)
    print('exit:', exit_dir)
    # Add reverse direction to reverse path
    reverse_path.append(reverse_dir[exit_dir])
    print('Reverse Path:', reverse_path)
    # Update previous room
    prev_room = current_room
    # Travel
    data = json.dumps(payload[exit_dir])
    print('Print json.dumps:', json.dumps(payload[exit_dir]))
    # p = requests.post(url + '/move/', headers=headers,
    #                   json={"direction": "n"})
    try:
        p = requests.post(url + '/move', headers=headers,
                          data=data)
        print('Post request:', p.json())
    except requests.exceptions.RequestException as e:
        print(e)
    print('Traveling...')
    cooldown = p.json()['cooldown']
    sleep(cooldown + 8)
    # Wait for cooldown
    # if cooldown < 15:
    #     sleep(cooldown + 15)
    #     print('Waiting...')
    # else:
    #     sleep(cooldown)
    #     print('Waiting...')

# Save graph to text file
with open('graph.txt', 'w') as f:
    f.write(graph)

# Save rooms to text file
with open('rooms.txt', 'w') as f:
    f.write(rooms)
