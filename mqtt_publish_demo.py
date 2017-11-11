import paho.mqtt.publish as publish
import time

print("Turning the Led on")
publish.single("CoreElectronics/test","On",hostname="test.mosquitto.org")

time.sleep(5)

print("Turning the led off")
publish.single("CoreElectronics/topic","Off",hostname="test.mosquitto.org")

print("Done")