import pyfirmata
import FunctionBackLog as fbl
import time

# verbinden met de arduino
arduino = pyfirmata.Arduino('COM5')

# pins
entryButtonPin = arduino.get_pin('d:2:i')
exitButtonPin = arduino.get_pin('d:3:i')

errorLedPin = arduino.get_pin('d:10:o')
startLedPin = arduino.get_pin('d:11:o')

# iterator starten
it = pyfirmata.util.Iterator(arduino)
it.start()

#maximale queue lengte
maxQueue = 10

# start led aan
startLedPin.write(1)
errorLedPin.write(1)

# lcd scherm aanmaken
lcd = fbl.lCDscreen(arduino)

# queue aanmaken
queue = fbl.QueueSystem(entryButtonPin, exitButtonPin, lcd,maxQueue,errorLedPin)
  

try:
    while True:
        queue.CheckButtonsAndUpdateQueue()
        time.sleep(.1) 

except KeyboardInterrupt:
    startLedPin.write(0)
    errorLedPin.write(0)
    lcd.clear()
    arduino.exit() 
