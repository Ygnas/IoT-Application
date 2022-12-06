#!/usr/bin/env python

from urllib.parse import urlparse
import paho.mqtt.client as mqtt
import asyncio
import websockets
import firebase_admin
from firebase_admin import credentials, storage, db
import os
from datetime import datetime

connected = set()
reply = "Can Be Opened"

cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pipi-6383e.appspot.com',
    'databaseURL':'https://pipi-6383e-default-rtdb.europe-west1.firebasedatabase.app/'
})

bucket = storage.bucket()

ref = db.reference('/')
home_ref = ref.child('gate_log')

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")


def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Connect
mqttc.connect("192.168.0.138", 1883)
mqttc.loop_start()

async def echo(websocket, path):
    global reply
    connected.add(websocket)
    try:
        await broadcast(0)
        # Broadcast a message to all connected clients.
        async for message in websocket:
            mqttc.publish("gates", "off")
            push_db("Gate Open")
            reply = "Openning"
            print("Received: " + message)
            await broadcast(15)
            reply = "Can Be Opened"
            await broadcast(0)
    except:
        # When android app is force closed print this.
        print("\nClient Disconnected\n")
    finally:
        # Unregister.
        connected.remove(websocket)

async def broadcast(delay):
    websockets.broadcast(connected, reply)
    await asyncio.sleep(delay)

def push_db(message):
    # Gets day time in nice string format
    now = datetime.now()
    daytime = now.strftime("%d/%m/%Y %H:%M:%S")

    # Push file reference to image in Realtime DB
    home_ref.push({
        'message': message,
        'timestamp': daytime}
    )

asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '0.0.0.0', 8000))
asyncio.get_event_loop().run_forever()