import pyfirmata
import FunctionBackLog as fbl
import time

# verbinden met de arduino
arduino = pyfirmata.Arduino('COM5')

# pins
entryButtonPin = arduino.get_pin('d:2:i')
exitButtonPin = arduino.get_pin('d:3:i')

errorLedPin = arduino.get_pin('d:7:o')
startLedPin = arduino.get_pin('d:8:o')

# iterator starten
it = pyfirmata.util.Iterator(arduino)
it.start()

maxQueue = 90
# start led aan
startLedPin.write(1)

# lcd scherm aanmaken
lcd = fbl.lCDscreen(arduino)

# queue aanmaken
queue = fbl.QueueSystem(entryButtonPin, exitButtonPin, lcd,maxQueue)
  
# main loop
while True:
    queue.CheckButtonsAndUpdateQueue()
    time.sleep(.1) 

# arduino afsluiten
arduino.exit() 
