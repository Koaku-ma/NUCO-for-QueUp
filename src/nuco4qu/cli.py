import requests


def main():
    ROOM_ENDPOINT = "https://api.queup.net/room/"
    CHAT_ENDPOINT = "https://api.queup.net/chat/"

    room_name = input("Enter room name: ")

    resp = requests.get(ROOM_ENDPOINT + room_name)
    room_id = resp.json()["data"]["_id"]

    resp = requests.get(CHAT_ENDPOINT + room_id)

    for msgObj in resp.json()["data"]:
        print(msgObj["user"]["username"] + ": " + msgObj["message"])
