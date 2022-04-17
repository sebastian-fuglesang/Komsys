import paho.mqtt.client as mqtt
import logging
from threading import Thread
import json
from appJar import gui
import appStyle as style
import webbrowser
from stmpy import Machine, Driver

#Kopierte kode fra app.py inn i appHomeController

# TODO: choose proper MQTT broker address
MQTT_BROKER='mqtt.item.ntnu.no'
MQTT_PORT=1883

# TODO: choose proper topics for communication
MQTT_TOPIC_INPUT='ttm4115/team07/mainApp'
MQTT_TOPIC_OUTPUT='ttm4115/team07/mainApp'



class SuperAwesomeApp:
    """
    The component to send voice commands.
    """

    def announceAvailable(self):
        print("hei hei jeg er tilgjengelig")
        homeController.announce_available() #kaller announce_available i homeController når en trykker på knappen tilgjengelig

    def announceUnavailable(self):
        self.publish_command("Unavailable")
        print("hei hei jeg er ikke tilgjengelig")
        homeController.announce_unavailable() #kaller announce_unavailable i homeController når en trykker på knappen utilgjengelig

    def publish_command(self, command):
        payload=json.dumps(command)
        self._logger.info(command)
        self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)

    def acceptCall(self):
        #An variable where True is accept call and False is refuse call
        global videoResponse
        if self.getting_called:
            self.getting_called=False
            #Global variable to be used in homeController state machine
            videoResponse=True
            print("Videoresponse true")
            self.app.setButtonBg("Aksepter samtale", "grey")
            self.app.setButtonBg("Nekt samtale", "grey")
            homeController.respond_to_call() #kaller homeController sin funksjon respond_to_call som trigger tilstandsendring
            webbrowser.get('/usr/bin/google-chrome %s &').open_new(
                'https://test-of-heroku2222.herokuapp.com/' + self.most_recent_room[2:-1])

    def refuseCall(self):
        global videoResponse
        if self.getting_called:
            self.getting_called=False
            # Global variable to be used in homeController state machine
            videoResponse=False
            self.app.setButtonBg("Aksepter samtale", "grey")
            self.app.setButtonBg("Nekt samtale", "grey")
            homeController.respond_to_call() #kaller homeController sin funksjon respond_to_call som trigger tilstandsendring

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {} with payload: {}".format(msg.topic, msg.payload))
        print(msg.payload)
        if (msg.topic == "ttm4115/team07/calls"):
            self.most_recent_room=str(msg.payload)
            self.getting_called=True
            self.app.setButtonBg("Aksepter samtale", "green")
            self.app.setButtonBg("Nekt samtale", "red")
            homeController.stm.send('call_invite') #sender trigger call_invite for å endre tilstand til respond_to_call

    def __init__(self):
        # get the logger object for the component
        self._logger=logging.getLogger(__name__)
        print('logging under name {}.'.format(__name__))
        self._logger.info('Starting Component')
        self.most_recent_room=""
        self.getting_called=False

        # create a new MQTT client
        self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
        self.mqtt_client=mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect=self.on_connect
        self.mqtt_client.on_message=self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # Subscribe to administrative topics
        self.mqtt_client.subscribe("ttm4115/team07/calls")
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        self.create_gui()

    def create_gui(self):
        self.app=gui(**style.body)
        self.app.addLabel("title", "Welcome to Super Awesome App")
        self.app.addButton('Tilgjengelig', self.announceAvailable)
        self.app.addButton('Utilgjengelig', self.announceUnavailable)
        self.app.addButton("Aksepter samtale", self.acceptCall)
        self.app.addButton("Nekt samtale", self.refuseCall)
        self.app.setButtonBg("Aksepter samtale", "grey")
        self.app.setButtonBg("Nekt samtale", "grey")
        self.app.setButtonBg("Tilgjengelig", "grey")
        self.app.setButtonBg("Utilgjengelig", "grey")

        #self.app.go()
        #Kommenterte ut det ovenfor fordi jeg ønsker å starte gui etter state machinen er startet

    #Lagde egen funksjon for å starte gui   
    def start_gui(self):
        self.app.go()

    def stop(self):
        """
        Stop the component.
        """
        # stop the MQTT client
        self.mqtt_client.loop_stop()

class HomeController:

    def init(self):
        print('Start up!')
        print(self.stm.driver.print_status())

    def announce_available(self):
        print('Available for Video call')
        print(self.stm.driver.print_status())
        t.publish_command("Available") #publiserer available via MQTT


    def announce_unavailable(self):
        print('Unavailable for Video call')
        print(self.stm.driver.print_status())
        t.publish_command("Unavailable") #publiserer unavailable via MQTT

    def respond_to_call(self):
        print('In Response to call state')
        print(self.stm.driver.print_status())
        self.stm.send('call_response') #aktiverer triggeren call_response


    def start_video_stream(self):
        print('Start Video stream')
        print(self.stm.driver.print_status())

    # Code for the compound transition:
    def respond_call_transition(self):
        if videoResponse==True:
            return 'callActive'
        else:
            return 'idle'

#Kun for testing av to state machines i samme koden
class GameController:

    def init(self):
        print('Start Game')
        print(self.stm.driver.print_status())

    def no_game(self):
        print('Not any game ongoing')
        print(self.stm.driver.print_status())

    def status_game(self):
        print('Game ongoing')
        print(self.stm.driver.print_status())


if __name__ == "__main__":
    driver = Driver()

    #Make an object of HomeController() and GameController()
    homeController = HomeController()
    #GameController is just for testing
    gameController = GameController()

    videoResponse = False 

    #homeController Transitions:
    t0 = {'source':'initial',  'target':'idle'}
    t1 = {'trigger':'call_invite', 'source':'idle', 'target':'respondToCall'}
    t2 = {'trigger':'call_response', 'source':'respondToCall', 'function':homeController.respond_call_transition}
    t3 = {'trigger':'play_game', 'source':'callActive', 'target':'callActive'}
    t4 = {'trigger':'leave', 'source':'callActive', 'target':'idle', 'effect':'stop_stream'}
    t5 = {'trigger':'t', 'source':'callActive', 'target':'idle', 'effect':'stop_stream'}

    # We declare dicts for the homeController states
    initial = {'name': 'initial',
        'entry': 'init()'}

    idle = {'name': 'idle',
        'entry': 'announce_available()', 'exit': 'announce_unavailable()'}

    respondToCall = {'name': 'respondToCall'}

    callActive = {'name': 'callActive',
        'entry': 'start_video_stream()'}



    #Make state machines of homeController:
    stm_homeController = Machine(transitions=[t0, t1, t2, t3, t4, t5], obj=homeController, states=[idle,respondToCall,callActive], name='stm_homeController')
    homeController.stm = stm_homeController

    driver.add_machine(stm_homeController)

    #gameController Transitions:
    t0 = {'source':'initial',  'target':'no_game'}
    t1 = {'trigger':'start_game', 'source':'no_game', 'target':'started_game'}
    t2 = {'trigger':'end_game', 'source':'started_game', 'target':'no_game'}

    # We declare dicts for the gameController states
    no_game = {'name': 'no_game', 'entry': 'no_game()'}
    started_game = {'name': 'started_game', 'entry': 'status_game()'}

    #Make state machines of homeController:
    stm_gameController = Machine(transitions=[t0, t1, t2], obj=gameController, states=[no_game,started_game], name='stm_gameController')
    gameController.stm = stm_gameController

    driver.add_machine(stm_gameController)



    # logging.DEBUG: Most fine-grained logging, printing everything
    # logging.INFO:  Only the most important informational log items
    # logging.WARN:  Show only warnings and errors.
    # logging.ERROR: Show only error messages.
    debug_level=logging.DEBUG
    logger=logging.getLogger(__name__)
    logger.setLevel(debug_level)
    ch=logging.StreamHandler()
    ch.setLevel(debug_level)
    formatter=logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    t=SuperAwesomeApp()


    gameController.mqtt_client = t.mqtt_client #...
    t.mqtt_client.stm_driver = driver


    driver.start()


    t.start_gui() #starts the gui after driver.start 

    driver.wait_until_finished()