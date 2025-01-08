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

# Dit is een class die doormiddel van de wachtrij theorie de wachttijd berekent

# I: aankomstsnelheid
# m: verwerkingssnelheid
# T: totale tijd
# W: wachttijd in de wachtrij
# S: servicetijd
# N: aantal personen in het systeem
# g: bezettingsgraad
class QueuingTheory:
    def __init__(self, I, m):
        self.I = I  
        self.m = m  
        self.people_in_queue = 0
        self.W = 0  # Initialize W
        self.update_wachttijd()

    def add_person(self):
        self.people_in_queue += 1
        self.update_wachttijd()

    def remove_person(self):
        if self.people_in_queue > 0:
            self.people_in_queue -= 1
        self.update_wachttijd()

    def update_wachttijd(self):
        if self.m == 0:
            raise ValueError("Verwerkings snelheid mag niet 0 zijn.")
        
        
        g = self.I/self.m # G = I / M
        
        T = self.people_in_queue / self.I # T = N / I
        S = 1 / self.m # S = 1 / M
        self.W = T - S # W = T - S
        

    def wachttijd(self):
        return self.W

#queuesystem class
class QueueSystem:
    def __init__(self, entry_button_pin, exit_button_pin, lcd_display, max_people_in_queue=90,I=1,m=1):
        self.people_in_queue = 0
        self.max_people_in_queue = max_people_in_queue
        self.entry_button_pin = entry_button_pin
        self.exit_button_pin = exit_button_pin
        self.lcd = lcd_display
        self.queuing_theory = QueuingTheory(I, m)
        self.updateDisplay()

    def updateDisplay(self):
        self.lcd.clear()
        self.lcd.write(0, f"Mensen in rij {self.people_in_queue}")
        self.lcd.write(1, f"Wachttijd: {self.queuing_theory.wachttijd():.2f} min")

    def AddPeopleToQueue(self):
        if self.people_in_queue >= self.max_people_in_queue:
            self.people_in_queue = self.max_people_in_queue
            self.lcd.clear()
            self.lcd.write(0, "Rij is vol!!")
            self.lcd.write(1, "kom later terug")
        else:
            self.people_in_queue += 1
            self.queuing_theory.add_person()
            self.updateDisplay()

    def RemovePeopleFromQueue(self):
        if self.people_in_queue <= 0:
            self.people_in_queue = 0
            self.updateDisplay()
        else:
            self.people_in_queue -= 1
            self.queuing_theory.remove_person()
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


