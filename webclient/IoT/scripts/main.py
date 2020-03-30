import pycom
from machine import UART, Pin, ADC
from LTR329ALS01 import LTR329ALS01
import ujson as json
import urequests as requests
import utime as time

pycom.heartbeat(False) # Don't let the heartbeat LED interfere with the light sensor

#
# USB Serial initialization
#
uart = UART(0)                               # init with given bus
uart.init(115200, bits=8, parity=None, stop=1) # init with given parameters:  Baudrate=9600


#
# Light sensor initialization
#
integration_time = LTR329ALS01.ALS_INT_50 # Integration time of the light sensor.
measurement_rate = LTR329ALS01.ALS_RATE_50 # A lower rate means higher sampling rate i.e. ALS_50 is quick, ALS_2000 is slow.
                                            # MUST be equal or larger than integration time
gain = LTR329ALS01.ALS_GAIN_1X # A higher gain means a more precise measures in the lower end i.e. 8X gives a range [0.125, 8K] lux

lightsensor = LTR329ALS01(integration=integration_time, rate=measurement_rate, gain=gain)


#
# Temperature sensor initialization
#
adc = ADC() # Analog to Digital converter used to read the temperature from the thermistor
blue_pin = adc.channel(pin='P16', attn=2) # Data pin (V_out pin on Thermistor), attn is the attenuation level
                                            # If attn=0, then the reading of the pin will be too high. attn=3 will lower the reading to the expected output from the thermistor.
p_red = Pin('P19', mode=Pin.OUT) # Use this pin to feed voltage to the Thermistor (V_dd pin on the Thermistor)
p_red.value(1) # Set the pin to HIGH i.e. output a current to the Thermistor


#
# API configuration
#
api_endpoint = 'http://iot.christianclausen.dk/iot/upload' # Production
transmission_counter = 0 # Message counter that gets incremented for each message that has potentially been emitted

while True:
    lux = lightsensor.light()  # light() provides a tuple of lux values. The light sensor is a dual light sensor, hence two values.
    luxC1 = lux[0]

    # Breaks the while loop if the ambient sensor is directly affected by light e.g. a flash light
    # Mechanism used to get control over the serial connection if new code should be uploaded.
    # This is to avoid safe booting by using a jumping cable between 3v3 and P12
    if (luxC1 > 12000):
        break

    temperature = blue_pin() # Read temperature sensor value

    body = json.dumps({
        u"iotdeviceid": u"IoT-chcla15",
        u"timestamp": time.time() * 1000, # Time in miliseconds. The time() method requires that the device is synced with an NTP (time) server in the boot.py file.
        u"transmissionscounter": transmission_counter,
        u"measurements": [
            {
                u"sensortype": u"light",
                u"value": int(luxC1)
            },
            {
                u"sensortype": u"temperature",
                u"value": temperature
            }
        ]
    })

    transmission_counter = transmission_counter + 1 # Increase the counter

    try:
        r = requests.post(api_endpoint, data=body,
                          headers={"Content-Type": "application/json",
                                   "User-Agent": "My User Agent 1.0"}) # User agent must be set, or you get a response: 406.0 - ModSecurity Action from ASP CORE

        print(r.status_code)
        print(r.text)
    except:
        # Ignore and continue
        print("Error when sending POST")

    time.sleep(1)  # Time to sleep in seconds

print("Exited main loop...")