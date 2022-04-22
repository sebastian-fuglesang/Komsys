from stmpy import Machine, Driver
from threading import Thread
import paho.mqtt.client as mqtt
from IPython.display import display

#MQTT:

#Kopierte mqtt-koden fra jupyter og justerte den litt mhp subscribing. 
#Må evnt finne ut hvilke meldinger vi skal ha i mqtt

broker, port="mqtt.item.ntnu.no", 1883

class MQTT_Client_1:
    def __init__(self):
        self.count = 0
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("on_connect(): {}".format(mqtt.connack_string(rc)))

    def on_message(self, client, userdata, msg):
        print("on_message(): topic: {}".format(msg.topic))
        print("Recieved message: "+str(msg.payload,'UTF-8')) 
        self.stm_driver.send("start_game", "stm_playGame") #start_game er triggeren. Dette er bare for testing

    def start(self, broker, port):

        print("Connecting to {}:{}".format(broker, port))
        self.client.connect(broker, port)

        self.client.subscribe([("ttm4115/team07/game/gameInvite",0), ("ttm4115/team07/game/command",0)])
        try:
            thread = Thread(target=self.client.loop_forever)
            thread.start()
        except KeyboardInterrupt:
            print("Interrupted")
            self.client.disconnect()

#Actions:

class HomeController:

    def init(self):
        print('Start up!')
        print(self.stm.driver.print_status())

    def announce_available(self):
        print('Available for Video call')
        print(self.stm.driver.print_status())
        self.stm.send('call_invite') #sender trigger, skal da skifte tilstand
        #MQTT Announce to server of availability

    def announce_unavailable(self):
        print('Unavailable for Video call')
        print(self.stm.driver.print_status())
        # MQTT Announce to server of unavailability?

    #bruker denne til å teste at jeg faktisk kommer inn i tilstanden respond to call:
    def respond_to_call(self):
        print('In Response to call state')
        print(self.stm.driver.print_status())
        self.stm.send('call_response') #sender trigger for å komme i ny tilstand

    def start_video_stream(self):
        print('start stream')
        print('Print gameController status')
        self.stm.driver.send('start_game', 'stm_PlayGame') #en test på at en kan sende en trigger til den andre state machinen
        playGame.mqtt_client.publish("ttm4115/team07/game/gameInvite", "start_game", 1) #en test på å publisere noe på mqtt
        print(self.stm.driver.print_status())
     
    # Code for the compound transition:
    def respond_call_transition(self):
        response=True #denne må settes i koden som kjøres i staten respond to call 
        if response==True:
            return 'callActive'
        else:
            return 'idle'

#Lagde denne for å teste å ha to state machines, en egen for playgame. 
#Vet ikke om dette er nødvendig..
class PlayGame:
    
    def init(self):
        print('Start Game')
        print(self.stm.driver.print_status())
        
    def no_game(self):
        print('Not any game ongoing')
        print(self.stm.driver.print_status())
        self.mqtt_client.publish("game")

    def play_game(self):
        print('Game ongoing')
        print(self.stm.driver.print_status())
    

driver = Driver()

#Make an object of HomeController()
homeController = HomeController()

playGame = PlayGame()

#homeController Transitions:

t0 ={'source':'initial',  'target':'idle'}
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

respondToCall = {'name': 'respondToCall', 'entry': 'respond_to_call()'}

callActive = {'name': 'callActive',
       'entry': 'start_video_stream()'}



#Make state machines:

stm_homeController = Machine(transitions=[t0, t1, t2, t3, t4, t5], obj=homeController, states=[idle,respondToCall,callActive], name='stm_homeController')
homeController.stm = stm_homeController

driver.add_machine(stm_homeController)

#PlayGame Transitions:


t0 = {'source':'initial',  'target':'no_game'}
t1 = {'trigger':'start_game', 'source':'no_game', 'target':'started_game'}
t2 = {'trigger':'end_game', 'source':'started_game', 'target':'no_game'}


# We declare dicts for the PlayGame states

no_game = {'name': 'no_game', 'entry': 'no_game()'}
started_game = {'name': 'started_game', 'entry': 'play_game()'}

stm_playGame = Machine(transitions=[t0, t1, t2], obj=playGame, states=[no_game,started_game], name='stm_playGame')

playGame.stm = stm_playGame

driver.add_machine(stm_playGame)

myclient = MQTT_Client_1()
playGame.mqtt_client = myclient.client
myclient.stm_driver = driver

myclient.start(broker, port)

driver.start()
driver.wait_until_finished()