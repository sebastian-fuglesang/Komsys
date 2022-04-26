from subprocess import Popen
from turtle import home
import paho.mqtt.client as mqtt
import logging
from threading import Thread
import json
from appJar import gui
import appStyle as style
import webbrowser
from stmpy import Machine, Driver
import webbrowser
import os
#from writeToDatabase import db

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
        self.app.setButtonBg("Tilgjengelig", "grey")
        self.app.setButtonBg("Utilgjengelig", "green")
        self.app.setLabel("STATUS", "STATUS: Tilgjengelig")
        self.mqtt_client.subscribe("ttm4115/team07/calls")  # subscribe via MQTT I'm available
        homeController.announce_available() #kaller announce_available i homeController når en trykker på knappen tilgjengelig

    def announceUnavailable(self):
        self.publish_command("Unavailable")
        print("hei hei jeg er ikke tilgjengelig")
        self.app.setButtonBg("Tilgjengelig", "green")
        self.app.setButtonBg("Utilgjengelig", "grey")
        self.app.setLabel("STATUS", "STATUS: Utilgjengelig")
        self.mqtt_client.unsubscribe("ttm4115/team07/calls")  # unsubscribe via MQTT I'm unavailable
        homeController.announce_unavailable() #kaller announce_unavailable i homeController når en trykker på knappen utilgjengelig

    def publish_command(self, command):
        payload=json.dumps(command)
        self._logger.info(command)
        self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)

    def acceptCall(self):
        #An variable where True is accept call and False is refuse call
        global videoResponse
        if self.getting_called and homeController.stm.state == 'respondToCall':
            self.getting_called=False
            #Global variable to be used in homeController state machine
            videoResponse=True
            print("Videoresponse true")
            homeController.respond_to_call() #kaller homeController sin funksjon respond_to_call som trigger tilstandsendring
            webbrowser.open_new(
                'https://heroku-call-service.herokuapp.com/' + self.most_recent_room[2:-1])
            self.app.setButtonBg("Aksepter samtale", "grey")
            self.app.setButtonBg("Nekt samtale", "grey")
            self.app.setButtonBg("Utilgjengelig", "grey")
            self.app.setButtonBg("Forlat samtale", "green")
            self.app.setLabel("STATUS", "STATUS: Active Video")
            self.mqtt_client.unsubscribe("ttm4115/team07/calls")  # unsubscribe via MQTT I'm in a video call
                

    def refuseCall(self):
        global videoResponse
        if self.getting_called and homeController.stm.state == 'respondToCall':
            self.getting_called=False
            # Global variable to be used in homeController state machine
            videoResponse=False
            self.app.setButtonBg("Aksepter samtale", "grey")
            self.app.setButtonBg("Nekt samtale", "grey")
            self.app.setButtonBg("Tilgjengelig", "green")
            self.app.setLabel("STATUS", "STATUS: Utilgjengelig")
            self.mqtt_client.unsubscribe("ttm4115/team07/calls")  # unsubscribe via MQTT I'm not accepting call
            homeController.respond_to_call() #kaller homeController sin funksjon respond_to_call som trigger tilstandsendring

    def leaveCall(self):
        if homeController.stm.state == 'callActive':
            stm_homeController.send('leave')
            print("Forlater videosamtalen...")
            self.app.setButtonBg("Tilgjengelig", "green")
            self.app.setButtonBg("Forlat samtale", "grey")
            self.app.setLabel("STATUS", "STATUS: Utilgjengelig")


    def getLeaderboard(self):
        print("Called play game")
        Popen(['python3', '/home/sebastfu/komsys/Komsys/app/leaderboard.py']) 
    
    def playGame(self):
        print("Called play game")
        Popen(['python3', '/home/sebastfu/komsys/Komsys/app/main.py', "False"])

        

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {} with payload: {}".format(msg.topic, msg.payload))
        print(msg.payload)
        if (msg.topic == "ttm4115/team07/calls" and homeController.stm.state == 'idle'):
            self.most_recent_room=str(msg.payload)
            self.getting_called=True
            self.app.setButtonBg("Aksepter samtale", "green")
            self.app.setButtonBg("Nekt samtale", "red")
            self.app.setButtonBg("Utilgjengelig", "grey")
            homeController.stm.send('call_invite') #sender trigger call_invite for å endre tilstand til respond_to_call
    
    def start_gui(self):
        self.app.go()

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
        self.mqtt_client.unsubscribe("ttm4115/team07/calls")
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
        self.app.addButton("Forlat samtale", self.leaveCall)
        self.app.addButton("Spill", self.playGame)
        self.app.addButton("Leaderboard", self.getLeaderboard)
        
        self.app.setButtonBg("Spill", "grey")
        self.app.setButtonBg("Leaderboard", "grey")
        self.app.setButtonBg("Aksepter samtale", "grey")
        self.app.setButtonBg("Nekt samtale", "grey")
        self.app.setButtonBg("Tilgjengelig", "green")
        self.app.setButtonBg("Utilgjengelig", "grey")
        self.app.setButtonBg("Forlat samtale", "grey")
        self.app.setButtonBg('Leaderboard', 'green')
        self.app.addLabel("STATUS", "STATUS: Utilgjengelig")
        
        #self.app.go()
        #Kommenterte ut det ovenfor fordi jeg ønsker å starte gui etter state machinen er startet

    #Lagde egen funksjon for å starte gui   
    

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


    def announce_unavailable(self):
        print('Unavailable for Video call')
        print(self.stm.driver.print_status())

    def respond_to_call(self):
        print('In Response to call state')
        print(self.stm.driver.print_status())
        self.stm.send('call_response') #aktiverer triggeren call_response


    def start_video_stream(self):
        print('Start Video stream')
        print(self.stm.driver.print_status())

    
    def stop_stream(self):
        print("Stop the video stream")
        os.system("taskkill /im chrome.exe /f") 
        print(self.stm.driver.print_status())
    

    # Code for the compound transition:
    def respond_call_transition(self):
        if videoResponse==True:
            return 'callActive'
        else:
            return 'idle'


if __name__ == "__main__":
    driver = Driver()

    #Make an object of HomeController() and GameController()
    homeController = HomeController()


    videoResponse = False 

    #homeController Transitions:
    t0 = {'source':'initial',  'target':'idle'}
    t1 = {'trigger':'call_invite', 'source':'idle', 'target':'respondToCall'}
    t2 = {'trigger':'call_response', 'source':'respondToCall', 'function':homeController.respond_call_transition}
    t3 = {'trigger':'play_game', 'source':'callActive', 'target':'callActive'}
    t4 = {'trigger':'leave', 'source':'callActive', 'target':'idle', 'effect':'stop_stream()'}

    # We declare dicts for the homeController states
    initial = {'name': 'initial',
        'entry': 'init()'}

    idle = {'name': 'idle',
        'entry': 'announce_available()', 'exit': 'announce_unavailable()'}

    respondToCall = {'name': 'respondToCall'}

    callActive = {'name': 'callActive',
        'entry': 'start_video_stream()'}



    #Make state machines of homeController:
    stm_homeController = Machine(transitions=[t0, t1, t2, t3, t4], obj=homeController, states=[idle,respondToCall,callActive], name='stm_homeController')
    homeController.stm = stm_homeController

    driver.add_machine(stm_homeController)


    debug_level=logging.DEBUG
    logger=logging.getLogger(__name__)
    logger.setLevel(debug_level)
    ch=logging.StreamHandler()
    ch.setLevel(debug_level)
    formatter=logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    t=SuperAwesomeApp()

    t.mqtt_client.stm_driver = driver


    driver.start()


    t.start_gui() #starts the gui after driver.start 

    driver.wait_until_finished()