# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Aprende e Ingenia                                            #
# 	Created:      2/26/2024, 6:59:41 PM                                        #
# 	Description:  EXP project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #
#vex:disable=repl

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# Motor config
brain_inertial = Inertial()
left_drive = Motor(Ports.PORT1, True)
right_drive = Motor(Ports.PORT5, True)
drivetrain = SmartDrive(left_drive, right_drive, brain_inertial, 259.34, 320, 40, MM, 1)

brain.screen.print("Gesture control")

def serial_monitor():
    try:
      s = open('/dev/serial1','rb')
    except:
      raise Exception('serial port not available')
    
    while True:
        data= s.read(1)
        print(data)
        if data == b'a' or data == b'A':
            brain.screen.print_at("forward", x=5, y=40)
            right_drive.spin(FORWARD, 50)
            left_drive.spin(REVERSE, 50)
        if data == b'r' or data == b'R':
            brain.screen.print_at("reverse", x=5, y=40)
            right_drive.spin(REVERSE, 50)
            left_drive.spin(FORWARD, 50)
        if data == b'd' or data == b'D':
            brain.screen.print_at("right  ", x=5, y=40)
            right_drive.spin(REVERSE, 50)
            left_drive.spin(REVERSE, 50)
        if data == b'i' or data == b'I':
            brain.screen.print_at("left   ", x=5, y=40)
            right_drive.spin(FORWARD, 50)
            left_drive.spin(FORWARD, 50)
        if data == b'p' or data == b'P':
            brain.screen.print_at("stop   ", x=5, y=40)
            right_drive.stop()
            left_drive.stop()
        
t1=Thread(serial_monitor)


        
