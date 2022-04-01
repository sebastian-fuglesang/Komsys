import paho.mqtt.client as mqtt
import logging
from threading import Thread
import json
from appJar import gui
import appStyle as style;

# TODO: choose proper MQTT broker address
MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

# TODO: choose proper topics for communication
MQTT_TOPIC_INPUT = 'ttm4115/team07/mainApp'
MQTT_TOPIC_OUTPUT = 'ttm4115/team07/mainApp'

class SuperAwesomeApp:
    """
    The component to send voice commands.
    """

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        pass

    def __init__(self):
        # get the logger object for the component
        self._logger = logging.getLogger(__name__)
        print('logging under name {}.'.format(__name__))
        self._logger.info('Starting Component')

        # create a new MQTT client
        self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        self.create_gui()
    

    def create_gui(self):
        self.app = gui(**style.body)

        def publish_command(command):
            payload = json.dumps(command)
            self._logger.info(command)
            self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)

        def announceAvailable():
            print("hei hei jeg er tilgjengelig")
            publish_command("Available")

        def announceUnavailable():
            publish_command("Unavailable")
            print("hei hei jeg er ikke tilgjengelig")

        def acceptCall():
            publish_command("accept_call")
            print("Aksepter samtale")

        def denyCall():
            publish_command("deny_call")
            print("Ikke aksepter samtale")
       
        self.app.addLabel("title", "Welcome to Super Awesome App")
        self.app.addButton('Tilgjengelig', announceAvailable)
        self.app.addButton('Utilgjengelig', announceUnavailable)
        self.app.addButton("Aksepter samtale", acceptCall)
        self.app.addButton("Nekt samtale", denyCall)
        self.app.go()


    def stop(self):
        """
        Stop the component.
        """
        # stop the MQTT client
        self.mqtt_client.loop_stop()


# logging.DEBUG: Most fine-grained logging, printing everything
# logging.INFO:  Only the most important informational log items
# logging.WARN:  Show only warnings and errors.
# logging.ERROR: Show only error messages.
debug_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

t = SuperAwesomeApp()