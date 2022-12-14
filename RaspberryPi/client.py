#!/usr/bin/env python

import asyncio
import os
import websockets
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import firebase_admin
from firebase_admin import credentials, storage
from picamera import PiCamera
from dotenv import load_dotenv

# serviceAccountKey.json is needed to be able to connect to firebase
cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'pipi-6383e.appspot.com'
})

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT")

def on_publish(client, obj, mid):
    print("Message ID: " + str(mid))

mqttc = mqtt.Client()
bucket = storage.bucket()
sense = SenseHat()
camera = PiCamera()

# Colours for sensehat to use
blue = (0,0,255)
red = (255,0,0)

# load_dotenv() will first look for a .env file and if it finds one, 
# it will load the environment variables from the file and make them 
# accessible to your project like any other environment variable would be.
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP")
SERVER_PORT = os.getenv("SERVER_PORT")
MQTT_IP = os.getenv("MQTT_IP")
MQTT_PORT = os.getenv("MQTT_PORT")

# Assign event callbacks
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish

# Connect to local Mosquitto broker
try:
    mqttc.connect(MQTT_IP, int(MQTT_PORT))
    mqttc.loop_start()
except:
    print("Could not connect to MQTT broker\n")

def store_file(fileLoc):
    try:
        filename=os.path.basename(fileLoc)
        blob = bucket.blob(filename) # Store File in Fb Bucket
        blob.upload_from_filename(fileLoc)
        print(f"{fileLoc} has been uploaded")
    except:
        # https://cloud.google.com/functions/quotas#time_limits
        # There is a function limit of 10 minutes, after that connection would be reset
        # And by getting the blob it aquires the connection so calling same function fixes it.
        print("Firebase connection lost. Reconnecting...")
        store_file(fileLoc)

async def client():
    # Formatted string literals are prefixed with 'f' and are similar to the format strings
    uri = f"ws://{SERVER_IP}:{SERVER_PORT}"
    async with websockets.connect(uri) as websocket:
        asyncio.get_running_loop()

        # Process messages received on the connection.
        async for message in websocket:
            # Sensehat shows blue 'O' when gates can be opened
            sense.show_letter("O", text_colour=blue)
            if (message == "Opening"):
                camera.capture("image.jpg")
                # Stores a file in firebase store
                store_file("image.jpg")
                # If no MQTT connection, new thread to process network traffic
                # is never started so it's safe to leave this one as is..?
                # IF there is a connection it will publish message 'off' on topic 'gates'
                mqttc.publish("gates", "off")
                # Sensehat display red 'X' when gates are opening
                sense.show_letter("X", text_colour=red)
                print("Received: " + message)

asyncio.run(client())