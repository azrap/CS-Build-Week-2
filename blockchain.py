import requests
import time
import hashlib
from random import randint
# from decouple import config

TOKEN = "a7af7d4d70b5e0f6d5032a265a84d496ac3b3d30"

headers = {"Authorization": "Token " + TOKEN}


def get_last_proof():
    res = requests.get(
        "https://lambda-treasure-hunt.herokuapp.com/api/bc/last_proof/",
        headers=headers
    )
    return res.json()


def mine(new_proof):
    res = requests.post(
        "https://lambda-treasure-hunt.herokuapp.com/api/bc/mine/",
        headers=headers,
        json={"proof": new_proof}
    )
    res_json = res.json()
    print(res_json)
    return res_json


def valid_proof(last_proof, proof, difficulty):
    check_proof = '0' * difficulty
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == check_proof


last_proof_obj = get_last_proof()
last_proof = last_proof_obj['proof']
diff = last_proof_obj['difficulty']
time.sleep(last_proof_obj['cooldown'])


def proof_of_work(start_point):
    print("Mining new block")

    start_time = time.time()
    proof = randint(-9876543210, 1234567890)
    while valid_proof(last_proof, proof, diff) is False:
        proof += 1

    end_time = time.time()
    print(
        f'Block mined in {round(end_time-start_time, 2)}sec. Nonce: {str(proof)}')

    print("Mining with proof...")
    response = mine(proof)
    return response


while True:
    res = proof_of_work(0)
    time.sleep(res["cooldown"])
