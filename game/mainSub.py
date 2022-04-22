import paho.mqtt.client as mqtt

MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

MQTT_TOPIC = 'ttm4115/team07/gameLobby'

def on_connect(client, userdata, flags, rc):
	print("Connection returned result: " + str(rc) )

def on_message(client, userdata, msg):
	print("on_message(): topic: {} with payload: {}".format(msg.topic, msg.payload))
	print(msg.topic+" "+str(msg.payload))

mqtt_client = mqtt.Client()
# callback methods
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
# Connect to the broker
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
#Subscribe to administrative topics
# start the internal loop to process MQTT messages
mqtt_client.loop_start()
#mqtt_client.subscribe(MQTT_TOPIC)