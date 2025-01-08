import pyfirmata
import FunctionBackLog as fbl
import time

# Establish a connection to the Arduino board
arduino = pyfirmata.Arduino('COM5')

entryButtonPin = arduino.get_pin('d:2:i')
exitButtonPin = arduino.get_pin('d:3:i')

errorLedPin = arduino.get_pin('d:11:o')
startLedPin = arduino.get_pin('d:12:o')

# Start an iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(arduino)
it.start()

lcd = fbl.lCDscreen(arduino)

queue = fbl.QueueSystem(entryButtonPin, exitButtonPin, lcd)

startLedPin.write(1)

while True:
    queue.CheckButtonsAndUpdateQueue()
    time.sleep(.1) 

arduino.exit() 
