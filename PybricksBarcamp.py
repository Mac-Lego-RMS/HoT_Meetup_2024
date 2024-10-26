from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor, ColorLightMatrix
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.geometry import Axis
from pybricks.tools import wait, StopWatch,  multitask, run_task
from pybricks.geometry import Matrix
from pybricks.tools import hub_menu
import urandom


#Definieren des Hubs und der Ausrichtung
# Hilfe für Achsen https://shorturl.at/AuDer
from pybricks.hubs import PrimeHub
hub = PrimeHub(top_side = -Axis.Z, front_side = Axis.Y)

# Möglichkeit der Umbelegung des Stop Buttons
hub.system.set_stop_button((Button.BLUETOOTH))

# Klasse Button ermöglicht es verschiedene Buttons abzufragen
left = Button.CENTER
right = Button.RIGHT
#Beispiel zum Überprüfen ob ein Button gedrückt wurde

while not any(pressed):
    pressed = hub.buttons.pressed()
    wait(10)

# Wait for all buttons to be released.
while any(hub.buttons.pressed()):
    wait(10)
if Button.RIGHT in pressed:
    double = True



#Initialisieren der Motoren
from pybricks.pupdevices import Motor

#Fahrmotoren: C & A
right_motor  = Motor(Port.A)
left_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE) #Andere Richtung, da Motor 180 Grad gedreht eingebaut ist

#Tool-Motoren: B & D
tool_front = Motor(Port.C)
tool_back  = Motor(Port.D)

#Grundsätzliche Motor Begriffe

# Grundsätzlich erster Wert ist Speed, zweiter Commandspezifisch
tool_back.run_angle(200,90) # Für eine bestimmten Winkel drehen
tool_back.run_target(200,190) # Auf einen bestimmten Winkel drehen
tool_back.run_time(-800,2000) # Für eine bestimmte Zeit drehen
tool_back.run_until_stalled(200) # Solange drehen bis der Motor gestoppt wird bzw. auf eine bestimmtes Power Limit gestoppt wird
tool_back.run_until_stalled(200,duty_limit=80) # Bei 80% der maximal Leistung stoppt der Motor

#verschiedene Möglichkeiten wie der Motor nach dem Befehl reagieren soll
tool_back.run_angle(800,400,Stop.HOLD)
tool_back.run_angle(800,400,Stop.BRAKE)
tool_back.run_angle(800,400,Stop.COAST)
tool_back.run_angle(800,400,Stop.NONE)

tool_back.run_angle(800,400,wait=True) # Programm wartet bis Befehl komplett ausgeführt wurde
tool_back.run_angle(800,400,wait=False) # Programm macht weiter Motor dreht trotzdem auf 400 Grad

# Weitere Tools

angle = tool_back.angle()
tool_back.reset_angle()
tool_back.stop()



#Initialisieren der Drive_Base (Des gesamten Roboters als "Fahrgestell")
drive_base = DriveBase(
    right_motor,
    left_motor,
    wheel_diameter=56, #Raddurchmesser
    axle_track=96      #Abstand der Auflagepunkte
)
drive_base.settings(
    straight_speed=800, #Geradeaus Geschwindigkeit # 977 Maximum
    straight_acceleration=350, #Geradeaus Beschleunigung # 1000 Maximum
    turn_rate=150, #Dreh Geschwindigkeit    # 977 Maximum
    turn_acceleration=930 #Drehbeschleunigung # 1000 Maximum
)

#Den Gyro aktivieren um den PID zu nutzen
drive_base.use_gyro(True)
    #Tunen des PIDs
    #drive_base.heading_control.pid(kp,ki,kd,deadzone,integralrate)

#Grundsätzliche Befehle der Drive Base

drive_base.straight(500) # Geradeausfahrt über 500mm Länge

drive_base.turn(90) # Drehung um 90 Grad (gegen den Uhrzeigersinn)

drive_base.curve(300,125) # Kurve um 125 Grad mit einem Radius von 300mm

distance = drive_base.distance() # Gibt die gefahrene Distanz nach dem letzten Reset zurück
drive_base.reset() # Ausrichtung und Distanz werden zurückgesetzt

drive_base.stop() # Stoppt die Drive Base und den PID

stalled = drive_base.stalled() #Steckt die Drive Base fest (Stalled?)



#Sensor 
from pybricks.pupdevices import ColorSensor
right_color = ColorSensor(Port.E) #Initialisieren des Sensors
### Am Spike Prime sind die Ports F und E die schnellsten, deswegen empfiehlt es sich hier die Sensoren anzuschließen

if right_color.color(True) == Color.RED:
    drive_base.straight(500)
elif right_color.reflection() >= 80:
    drive_base.turn(-90)



# Nutzung des Hubs

print(hub.battery.voltage()) #in mV
print(hub.charger.status())

#hub.imu. ... Abfragen einiger Werte des Gyrosensors

hub.display.char("Z") # Anzeigen von Buchstaben auf Matrix. Gibt noch viele andere Möglichkeiten von display

hub.speaker.beep(1500,800)


# Menü mit Navigation
# Das ganze am besten in einem Main Loop da hier sich alles abspielt
while True:
    selected = hub_menu("H", "U", "3","Y","5","D","M","B","A")
    if selected == "H":
        drive_base.straight(200)

    if selected == "D":
        drive_base.turn(90)
        tool_back.run_angle(1000,424)



