import requests
import json
import time
import math
import random

api_endpoint = 'http://iot.christianclausen.dk/iot/upload' # Production
#api_endpoint = 'https://localhost:5001/iot/upload' # Development server

transmission_counter = 0 # The first message is message 0

while True:
    body = json.dumps({
        u"iotdeviceid": u"LaptopClient1",
        u"timestamp": int(time.time_ns() * math.pow(10, -6)),
        u"transmissionscounter": transmission_counter,
        u"measurements": [
            {
                u"sensortype": u"light",
                u"value": int((random.random()*15000+1)) # Random number from 0 to 15000
            },
            {
                u"sensortype": u"temperature",
                u"value": round(15+(random.random()*19), 2) # Random number from 15 to 34.99
            }
        ]
    })

    transmission_counter = transmission_counter + 1 # Increase the counter
    time.sleep(1) # Time to sleep in seconds

    try:
        r = requests.post(api_endpoint, data=body, verify=False, # Ignore self-signed certificate warnings
                      headers={"Content-Type": "application/json",
                               "User-Agent": "My User Agent 1.0"}) # User agent must be set, or you get a response: 406.0 - ModSecurity Action from ASP CORE
        print(r.status_code)
        print(r.text)
    except:
        # Ignore and continue
        print("Error when sending POST")


