from pyfirmata import Arduino
import time
LCD_PRINT = 0x01
LCD_CLEAR = 0x02
LCD_SET_CURSOR = 0x03

class lCDscreen:
    def __init__(self, arduino):
        self.arduino = arduino

    def clear(self):
        self.arduino.send_sysex(LCD_CLEAR, [0,0])

    def write(self,line:int,message:str):
        if line > 1: line = 1

        message_bytes = [ord(char) for char in message]

        # Set the cursor to the first position
        self.arduino.send_sysex(LCD_SET_CURSOR, [0, line])

        self.arduino.send_sysex(LCD_PRINT, message_bytes)


    # Clear the LCD
    # arduino.send_sysex(LCD_CLEAR, [])
class QueueSystem:
    def __init__(self, entry_button_pin, exit_button_pin, lcd_display, max_people_in_queue=90):
        self.people_in_queue = 0
        self.max_people_in_queue = max_people_in_queue
        self.entry_button_pin = entry_button_pin
        self.exit_button_pin = exit_button_pin
        self.lcd = lcd_display
        self.updateDisplay()

    def updateDisplay(self):
        self.lcd.clear()
        self.lcd.write(0, f"Mensen in rij {self.people_in_queue}")

    def AddPeopleToQueue(self):
        if self.people_in_queue >= self.max_people_in_queue:
            self.people_in_queue = self.max_people_in_queue
            self.lcd.clear()
            self.lcd.write(0, "Rij is vol!!")
            self.lcd.write(1, "kom later terug")
        else:
            self.people_in_queue += 1
            self.updateDisplay()

    def RemovePeopleFromQueue(self):
        if self.people_in_queue <= 0:
            self.people_in_queue = 0
            self.updateDisplay()
        else:
            self.people_in_queue -= 1
            self.updateDisplay()

    def isEntryButtonPressed(self):
        button_state = self.entry_button_pin.read()
        return button_state == 1
    
    def isExitButtonPressed(self):
        button_state = self.exit_button_pin.read()
        return button_state == 1

    def CheckButtonsAndUpdateQueue(self):
        if self.isEntryButtonPressed():
            self.AddPeopleToQueue()
            while self.isEntryButtonPressed():
                time.sleep(0.1)

        if self.isExitButtonPressed():
            self.RemovePeopleFromQueue()
            while self.isExitButtonPressed():
                time.sleep(0.1)