import asyncio
from datetime import datetime
import websockets
import json

REPO = dict()
REPO[1] = {'caseno': 2, 'ward': 'A091', 'name': '王大明', 'age': 25, 'bedno': 10,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[2] = {'caseno': 2, 'ward': 'A091', 'name': '王大明', 'age': 25, 'bedno': 10,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[3] = {'caseno': 2, 'ward': 'A092', 'name': '王大明', 'age': 25, 'bedno': 10,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}
REPO[4] = {'caseno': 2, 'ward': 'A092', 'name': '王大明', 'age': 25, 'bedno': 10,
           'section': 'PEDD', 'gender': '男', 'hr': [], 'rr': [], 'bt': [],
           'sat': [], 'sbp': [], 'gcs': [], 'device': []}

USERS = dict()   # {websocket :{subscribe_type, subscribe_content, patients}}

REPO[1]['hr'].append({'datetime': '2019-04-06 10:48:20', 'value': '80'})
REPO[1]['rr'].append({'datetime': '2019-04-06 10:48:20', 'value': '20'})
REPO[1]['bt'].append({'datetime': '2019-04-06 10:48:20', 'value': '37.5'})
REPO[1]['sbp'].append({'datetime': '2019-04-06 10:48:20', 'value': '101'})
REPO[1]['sat'].append({'datetime': '2019-04-06 10:48:20', 'value': '96'})
REPO[1]['gcs'].append({'datetime': '2019-04-06 10:48:20', 'value': 'E4V5M6'})
REPO[1]['device'].append(
    {'datetime': '2019-04-06 10:48:20', 'value': 'Non-invasive'})


def users_event():
    return json.dumps({'type': 'users', 'content': len(USERS)})


async def notify_users():
    if USERS:       # asyncio.wait doesn't accept an empty list
        message = users_event()
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    USERS[websocket] = {}
    await notify_users()


async def unregister(websocket):
    USERS.pop(websocket)
    await notify_users()


def getPatientCollection(ward):
    return [x for x in REPO if REPO[x]['ward'] == ward]


async def notify_patient_update(hisid):
    selected_USERS = []
    try:
        selected_USERS = [
            x for x in USERS
            if x in USERS and 'patients' in USERS[x] and hisid in USERS[x]
            ['patients']]
    finally:
        if selected_USERS:       # asyncio.wait doesn't accept an empty list
            await asyncio.wait([user.send(json.dumps({'type': 'patient', 'content': {'hisid': hisid, **REPO[hisid]}})) for user in selected_USERS])


async def subscribe(websocket, path):
    await register(websocket)
    try:
        async for message in websocket:
            print(message)
            print(websocket)
            message = json.loads(message)
            if message['action'] == 'subscribe':
                if message['type'] == 'ward':
                    patientCollection = getPatientCollection(message['content'])
                    USERS[websocket] = {
                        'subscribe_type': 'ward',
                        'subscribe_content': message['content'],
                        'patients': patientCollection}
                    await websocket.send(json.dumps({'type': 'patientcollection', 'content': [{'hisid': x, **REPO[x]} for x in patientCollection]}))
            print(USERS)
    except Exception as e:
        print('error', e)
    finally:
        await unregister(websocket)


async def timer():  # simulate patient update
    counter = 0
    while True:
        counter += 1
        REPO[1]['hr'] = [{'datetime': '2019-04-06 10:48:20', 'value': counter}]
        await notify_patient_update(1)
        await asyncio.sleep(1)


start_server_subscribe = websockets.serve(subscribe, port=5000)


asyncio.get_event_loop().run_until_complete(start_server_subscribe)
asyncio.get_event_loop().run_until_complete(timer())

asyncio.get_event_loop().run_forever()
