import requests
from decouple import config
from pprint import pprint


def main():
    LOGIN_ENDPOINT = "https://api.queup.net/auth/login"
    ROOM_ENDPOINT = "https://api.queup.net/room/"
    CHAT_ENDPOINT = "https://api.queup.net/chat/"

    room_name = config("ROOM_NAME", default=None)
    username = config("QU_USERNAME", default=None)
    password = config("QU_PASSWORD", default=None)
    message = config("QU_MESSAGE", default=None)

    if room_name is None:
        print("ROOM_NAME is not set")
        exit(1)
    if username is None:
        print("USERNAME is not set")
        exit(1)
    if password is None:
        print("PASSWORD is not set")
        exit(1)
    if message is None:
        print("MESSAGE is not set")
        exit(1)

    resp = requests.get(ROOM_ENDPOINT + room_name)
    if resp.status_code != 200:
        print("room not found")
        exit(1)
    room_id = resp.json()["data"]["_id"]

    resp = requests.get(CHAT_ENDPOINT + room_id)
    if resp.status_code != 200:
        print("chat not found")
        exit(1)

    for msgObj in resp.json()["data"]:
        print(msgObj["user"]["username"] + ": " + msgObj["message"])

    resp = requests.post(
        LOGIN_ENDPOINT,
        json={
            "username": username,
            "password": password,
        },
    )
    if resp.status_code != 200:
        print("login failed")
        exit(1)

    resp = requests.post(
        CHAT_ENDPOINT + room_id,
        json={
            "message": message,
        },
        cookies=resp.cookies,
    )
    if resp.status_code != 200:
        print("chat failed")
        exit(1)

    pprint(resp.json())
