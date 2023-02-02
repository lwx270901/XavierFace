import requests
from datetime import datetime
# api-endpoint
URL = "https://dacn-backend.vercel.app"

data = {
    "user": "638d93c98f710dd70f8d0fc0",
    "room": "638db57ad177d2cddc73dd05",
    "credential": "app-qr",
    "images": [
        {
            "name": "door-access-control-young-officer-woman-holding-key-card-lock-unlock-door-access-entry",
            "url": "https://img.freepik.com/premium-photo/door-access-control-young-officer-woman-holding-key-card-lock-unlock-door-access-entry_38678-5335.jpg"
        }
    ],
    "time": "2022-12-05T13:19:36.211Z"
}



def GetMethod(url, params):
    r = requests.get(url, params)
    data = r.json()
    return data

def PostMethod(url, params):
    r = requests.post(url, json=params)
    return r




res = GetMethod(URL + '/user/638d93c98f710dd70f8d0fc0' , params='')
if res['status_code'] == 200:
    #get ID
    user = res['data']['_id']
    room = '638db57ad177d2cddc73dd05'
    now = datetime.now()

    current_time = now.isoformat()
    time = current_time

    mess = {
        "user": user,
        "room" : room,
        "credential": "app-qr",
        "images": [
        {
            "name": "door-access-control-young-officer-woman-holding-key-card-lock-unlock-door-access-entry",
            "url": "https://img.freepik.com/premium-photo/door-access-control-young-officer-woman-holding-key-card-lock-unlock-door-access-entry_38678-5335.jpg"
        }
        ],
        "time": time
    }

    r = PostMethod(URL + '/access-event', mess)

print(r.json())