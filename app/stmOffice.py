import time
from appJar import gui
from stmpy import Machine, Driver
from motionDetectorTumbsup import motion_detector
import webbrowser
import os

class OfficeController:
    """
    State machine for the office controller
    """
    def __init__(self, component):
        self.component = component

    def create_GUI(self):
        self.app = gui()
        self.app.setOnTop()
        self.app.startLabelFrame('Office controller')

        def on_leave():
            os.system("taskkill /im chrome.exe /f")
            time.sleep(1)
            self.stm.send('leave_request')
            self.app.stop()
            print('Leaving room...')
        

        self.app.addButton('Leave', on_leave)
        self.app.setLocation(0, 200)
        self.app.go()

    def start_motion_detection(self):
        print('Motion detection started, waiting for motion...')

    def stop_motion_detection(self):
        print('Motion detected...')

    def request_room(self):
        try:
            webbrowser.open_new('https://heroku-call-service.herokuapp.com/')
            self.stm.send('server_request_ok')
            time.sleep(0.5)
            self.create_GUI()
        except:
            self.stm.send('server_request_bad')

    def send_video_stream(self):
        print('Video ongoing...')

    def start_motiondetector(self):
        motion_detector()
        self.stm.send('motion')


if __name__ == "__main__":
    officeController = OfficeController(None)

    t0 = {
        'source': 'initial',
        'target': 'idle'
    }

    #motion detected, initates call
    t1 = {
        'trigger': 'motion',
        'source': 'idle',
        'target': 'init_call'
    }

    #server request ok, videoroom ready and call active
    t2 = {
        'trigger': 'server_request_ok',
        'source': 'init_call',
        'target': 'call_active'
    }

    #server request fails, user sent back to idle
    t3 = {
        'trigger': 'server_request_bad',
        'source': 'init_call',
        'target': 'idle'
    }


    #user leaves, user is sent back to idle
    t4 = {
        'trigger': 'leave_request',
        'source': 'call_active',
        'target': 'idle'
    }

    #states

    idle = {
        'name': 'idle', 
        'entry': 'start_motiondetector',
        'exit': 'stop_motion_detection'
    }

    init_call = {
        'name': 'init_call',
        'entry': 'request_room'
    }

    call_active = {
        'name': 'call_active',
        'entry': 'send_video_stream'
    }


    stm = Machine(
        name='stm',
        transitions=[t0, t1, t2, t3, t4],
        obj=officeController,
        states=[idle, init_call, call_active]
    )

    officeController.stm = stm


    driver = Driver()
    driver.add_machine(stm)
    driver.start()

    #officeController.create_GUI()



