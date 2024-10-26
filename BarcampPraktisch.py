from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.geometry import Axis
from pybricks.tools import wait, StopWatch,  multitask, run_task
from pybricks.geometry import Matrix
from pybricks.tools import hub_menu
import urandom

#Initialization for the Spike and his Axis
hub = PrimeHub(top_side = -Axis.Z, front_side = Axis.Y)

#Current Voltage
print("Battery voltage: "+str(hub.battery.voltage()/1000)+" V")

# For Debugging:
DebugMode = True
if DebugMode:
    from usys import stdin
    from uselect import poll
    # Register the standard input so we can read keyboard presses.
    keyboard = poll()
    keyboard.register(stdin)

def debugWait():
    if DebugMode:
        hub.speaker.beep(500,100)
        while True:
            if keyboard.poll(0): # Check if a key has been pressed.
                # Read the key and print it.
                key = stdin.read(1)
                print("You pressed:", key)
                hub.speaker.beep(500,100)
                break
            if any(hub.buttons.pressed()):
                print("button continue")
                hub.speaker.beep(500,100)
                break
    #     debugWait()

################# Initialization Robot ####################



# Initialize both motors.
#Drive motors: C & A
right_drive  = Motor(Port.B)
left_drive = Motor(Port.D, Direction.COUNTERCLOCKWISE)

#Tool-motors: B & D
left_tool   = Motor(Port.E)
right_tool  = Motor(Port.A)

colorAttach = ColorSensor(Port.C)
colorBottom = ColorSensor(Port.F)

#Stop via Bluetooth Button
hub.system.set_stop_button((Button.BLUETOOTH))

#Initialize Drive Base
drive_base = DriveBase(
    right_drive,
    left_drive,
    wheel_diameter=62.4,
    axle_track=120
)
#Drive Base Settings
maxSpeed = 977
maxAcc = 1000

#Standard and Max Speed
maxSpeedSettings = [977,1000,150,930]
drive_base.settings(977,350,150,930)


# activate Drive Base Gyro (PID)
drive_base.use_gyro(True)

#Tune PID Controller
drive_base.heading_control.pid(kp=125000,ki=2400000)

# Brightness of the Matrix
h = 100

# Verschiedene Homezones
homezone1 = False

# Reset Heading/Gyro
hub.imu.reset_heading(0)

# Arrays for the Spike 5x5 Matrix (help for the technicians)
arrowBack = Matrix(
    [
    [0,0,h,0,0],
    [0,h,0,0,0],
    [h,h,h,h,h],
    [0,h,0,0,0],
    [0,0,h,0,0]
    ]
)
arrowFor = Matrix(
    [
    [0,0,h,0,0],
    [0,0,0,h,0],
    [h,h,h,h,h],
    [0,0,0,h,0],
    [0,0,h,0,0]
    ]
)

pfeil = Matrix(
    [
    [0,0,0,0,0],
    [0,h,0,h,0],
    [0,0,0,0,0],
    [h,0,0,0,h],
    [0,h,h,h,0]
    ]
)

left_right = Matrix(
    [
    [h,0,h,0,h],
    [h,0,h,0,h],
    [h,h,h,h,h],
    [0,0,0,0,0],
    [0,0,0,0,0]
    ]
)


#Musik
def Mario():
    s = 65
    hub.speaker.beep(392,s)
    hub.speaker.beep(494,s)
    hub.speaker.beep(587,s)
    hub.speaker.beep(784,s)
    hub.speaker.beep(988,s)

   # hub.speaker.beep(415,s)
    #hub.speaker.beep(523,s)
    #hub.speaker.beep(622,s)
    #hub.speaker.beep(831,s)
    #hub.speaker.beep(1047,s)

    #hub.speaker.beep(466,s)
    #hub.speaker.beep(587,s)
    #hub.speaker.beep(659,s)
    #hub.speaker.beep(932,s)
    #hub.speaker.beep(1175,s)


Mario()


# Wait until Button press
def waitBack(color):
    hub.light.animate([color,Color.NONE],200)
    hub.display.icon(arrowFor)
    while True:
        if any(hub.buttons.pressed()):
                        break

# Wait until Button press
def waitFor(color):
    hub.light.animate([color,Color.NONE],200)
    hub.display.icon(arrowBack)
    while True:
        if any(hub.buttons.pressed()):
                        break


