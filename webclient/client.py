import requests
import json
import time
import math
import random

api_endpoint = 'https://localhost:5001/iot/upload'

transmission_counter = 0 # The first message is message 0

while True:
    body = json.dumps({
        u"iotdeviceid": u"MyIoTDevice",
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

    r = requests.post(api_endpoint, data=body, verify=False, # Ignore self-signed certificate warnings
                      headers={"Content-Type": "application/json"})

    print(r.status_code)
    print(r.text)


