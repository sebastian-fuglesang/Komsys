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
from subprocess import Popen
from gameDBService import db

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
        self.app.setButtonBg("Tilgjengelig", "green")
        self.app.setButtonBg("Utilgjengelig", "grey")
        self.app.setLabel("STATUS", "STATUS: Tilgjengelig")
        self.mqtt_client.subscribe("ttm4115/team07/calls")  # subscribe via MQTT I'm available
        homeController.announce_available()

    def announceUnavailable(self):
        self.publish_command("Unavailable")
        self.app.setButtonBg("Tilgjengelig", "grey")
        self.app.setButtonBg("Utilgjengelig", "green")
        self.app.setLabel("STATUS", "STATUS: Utilgjengelig")
        self.mqtt_client.unsubscribe("ttm4115/team07/calls")  # unsubscribe via MQTT I'm unavailable
        homeController.announce_unavailable()

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
            homeController.respond_to_call()
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
            self.app.setButtonBg("Tilgjengelig", "grey")
            self.app.setButtonBg("Utilgjengelig", "green")
            self.app.setLabel("STATUS", "STATUS: Utilgjengelig")
            self.mqtt_client.unsubscribe("ttm4115/team07/calls")  # unsubscribe via MQTT I'm not accepting call
            homeController.respond_to_call()

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
        Popen(['py', r'C:\Users\sigur\Documents\Master\2_semester\Deisgn\sec2\Komsys\app\gameHome.py'])

        

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {} with payload: {}".format(msg.topic, msg.payload))
        print(msg.payload)
        print(homeController.stm.state)
        if (msg.topic == "ttm4115/team07/calls" and homeController.stm.state == 'available'):
            print("check")
            self.most_recent_room=str(msg.payload)
            self.getting_called=True
            self.app.setButtonBg("Aksepter samtale", "green")
            self.app.setButtonBg("Nekt samtale", "red")
            self.app.setButtonBg("Utilgjengelig", "grey")
            homeController.stm.send('call_invite')
 
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
        self.app.setButtonBg("Tilgjengelig", "grey")
        self.app.setButtonBg("Utilgjengelig", "green")
        self.app.setButtonBg("Forlat samtale", "grey")
        self.app.setButtonBg('Leaderboard', 'green')
        self.app.addLabel("STATUS", "STATUS: Utilgjengelig")

        #leaderboard subwindow
        self.app.startSubWindow('Leaderboard window', modal=True)
        data = db.readFromDatabase()
        self.app.addTable('table', [['Name', 'Wins']])
        self.app.addTableRows('table', data)
    

    def stop(self):
        """
        Stop the component.
        """
        # stop the MQTT client
        self.mqtt_client.loop_stop()

class HomeController:

    def announce_available(self):
        print('Available for Video call')
        self.stm.send('announce_available')
        print(self.stm.driver.print_status())

    def announce_unavailable(self):
        print('Unavailable for Video call')
        self.stm.send('announce_unavailable')
        print(self.stm.driver.print_status())

    def respond_to_call(self):
        print('In Response to call state')
        print(self.stm.driver.print_status())
        self.stm.send('call_response')


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
    t0 = {'source':'initial',  'target':'unavailable'}
    t1 = {'trigger':'call_invite', 'source':'available', 'target':'respondToCall'}
    t2 = {'trigger':'call_response', 'source':'respondToCall', 'function':homeController.respond_call_transition}
    t3 = {'trigger':'play_game', 'source':'callActive', 'target':'callActive'}
    t4 = {'trigger':'leave', 'source':'callActive', 'target':'available', 'effect':'stop_stream()'}
    t5 = {'trigger': 'announce_available', 'source': 'unavailable', 'target': 'available'}
    t6 = {'trigger': 'announce_unavailable', 'source': 'available', 'target': 'unavailable'}

    # We declare dicts for the homeController states
    unavailable = {'name': 'unavailable'}

    available = {'name': 'available'}

    respondToCall = {'name': 'respondToCall'}

    callActive = {'name': 'callActive',
        'entry': 'start_video_stream()'}

    #Make state machines of homeController:
    stm_homeController = Machine(transitions=[t0, t1, t2, t3, t4, t5, t6], obj=homeController, states=[unavailable, available, respondToCall,callActive], name='stm_homeController')
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
