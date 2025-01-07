import pyfirmata
import FunctionBackLog as fbl
import time

# Establish a connection to the Arduino board
arduino = pyfirmata.Arduino('COM5')

entryButtonPin = arduino.get_pin('d:2:i')
exitButtonPin = arduino.get_pin('d:3:i')

# Start an iterator thread to avoid buffer overflow
it = pyfirmata.util.Iterator(arduino)
it.start()

lcd = fbl.lCDscreen(arduino)

queue = fbl.QueueSystem(entryButtonPin, exitButtonPin, lcd)



while True:
    queue.CheckButtonsAndUpdateQueue()
    time.sleep(.1) 

arduino.exit() 
