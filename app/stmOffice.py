from appJar import gui
from stmpy import Machine, Driver
from motionDetectorTumbsup import motion_detector
class OfficeController:
    """
    State machine for the office controller
    """
    def __init__(self, component):
        self.component = component

    def create_GUI(self):
        self.app = gui()

        self.app.startLabelFrame('Office controller')

        def on_request_ok():
            self.stm.send('server_request_ok')
            print('Request OK...')

        def on_request_bad():
            self.stm.send('server_request_bad')
            print('ERROR, sendt back to idle...')

        def on_leave():
            self.stm.send('leave_request')
            print('Leaving room...')

        def on_timer():
            self.stm.send('t')
            print('Leaving room...')
        
        self.app.addButton('Server ok', on_request_ok)
        self.app.addButton('Server bad', on_request_bad)
        self.app.addButton('Timer', on_timer)
        self.app.addButton('Leave', on_leave)
        
        self.app.go()

    def start_motion_detection(self):
        print('Motion detection started, waiting for motion...')

    def stop_motion_detection(self):
        print('Motion detected...')

    def request_room(self):
        print('Requesting room from signaling server...')

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

    #timer times out, room is closed and user is sent back to idle
    t4 = {
        'trigger': 't',
        'source': 'call_active',
        'target': 'idle'
    }

    #user leaves, user is sent back to idle
    t5 = {
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
        transitions=[t0, t1, t2, t3, t4, t5],
        obj=officeController,
        states=[idle, init_call, call_active]
    )

    officeController.stm = stm


    driver = Driver()
    driver.add_machine(stm)
    driver.start()

    officeController.create_GUI()



