from pyfirmata import Arduino
import FunctionBackLog as fbl
from time import sleep
# Establish a connection to the Arduino board
arduino = Arduino('COM5')

lcd = fbl.LCDscherm(arduino)

# Define the string to print
test = "test"

lcd.write(0,test)
lcd.write(1,test)

# Close the connection to the board
arduino.exit()

class Main:
    def __init__(self,arduino_port,):
        self._arduinoport = arduino_port
        