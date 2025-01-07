from pyfirmata2 import Arduino, util
import time

board = Arduino('COM5') 
Rood_pin = 8
Oranje_pin = 9
Groen_pin = 10


startTimerGreen = 0
startTimerOrange = 0
waitTimeGreen = 5
waitTimeOrange = 5

StopLicht = "Red"


while True:
    CurrentTime = time.time()

    match StopLicht:
        case 'Red':
            board.digital[Rood_pin].write(1)
            AutoChecker = input("Is er een auto? (Y)")
            if AutoChecker == 'Y':
                board.digital[Rood_pin].write(0)
                board.digital[Groen_pin].write(1)
                print("Auto gedetecteerd")    
                StopLicht = "Green"
                startTimerGreen = CurrentTime
                print("Groen")
        case 'Green':
            if CurrentTime - startTimerGreen > waitTimeGreen:
                board.digital[Groen_pin].write(0)
                board.digital[Oranje_pin].write(1)
                StopLicht = "Orange"
                startTimerOrange = CurrentTime
                print("Oranje")
        case 'Orange':
            if CurrentTime - startTimerOrange > waitTimeOrange:
                board.digital[Oranje_pin].write(0)
                StopLicht = "Red"

