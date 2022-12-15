#!/usr/bin/env python

import os
from urllib.parse import urlparse
import asyncio
import websockets
import firebase_admin
from firebase_admin import credentials, storage, db
from datetime import datetime
from dotenv import load_dotenv

connected = set()
reply = "Can Be Opened"

# serviceAccountKey.json is needed to be able to connect to firebase
cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pipi-6383e.appspot.com',
    'databaseURL':'https://pipi-6383e-default-rtdb.europe-west1.firebasedatabase.app/'
})

# load_dotenv() will first look for a .env file and if it finds one, 
# it will load the environment variables from the file and make them 
# accessible to your project like any other environment variable would be.
load_dotenv()

SERVER_PORT = os.getenv("SERVER_PORT")

bucket = storage.bucket()

ref = db.reference('/')
home_ref = ref.child('gate_log')

async def echo(websocket, path):
    # So it would use global reply variable and not make one local to the function
    global reply
    # Adds clients to connected clients
    connected.add(websocket)
    try:
        await broadcast(0)
        # Broadcast a message to all connected clients.
        async for message in websocket:
            if (message == "open"):
                # Sends data to firebase with message
                push_db("Gate Open")
                reply = "Opening"
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

# Broadcasts message to all clients connected
async def broadcast(delay):
    websockets.broadcast(connected, reply)
    await asyncio.sleep(delay)

def push_db(message):
    # Gets day time in nice string format
    now = datetime.now()
    daytime = now.strftime("%d/%m/%Y %H:%M:%S")

    # Push file reference to gate_log in Realtime DB
    home_ref.push({
        'message': message,
        'timestamp': daytime}
    )

asyncio.get_event_loop().run_until_complete(websockets.serve(echo, '0.0.0.0', SERVER_PORT))
asyncio.get_event_loop().run_forever()