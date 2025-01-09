from pyfirmata import Arduino
import time
LCD_PRINT = 0x01
LCD_CLEAR = 0x02
LCD_SET_CURSOR = 0x03

# Dit is een class die de LCD scherm aanstuurt
# variabel bij de init:
# arduino is de arduino die de lcd scherm aanstuurt

# functies:
# clear() zorgt ervoor dat het scherm leeg is
# write() zorgt ervoor dat er tekst op het scherm komt
class lCDscreen:
    def __init__(self, arduino):
        self.arduino = arduino

    def clear(self):
        # clear scherm
        self.arduino.send_sysex(LCD_CLEAR, [0,0])

    def write(self,line:int,message:str):
        # check of line 0 of 1 is
        if line > 1: line = 1

        # bericht omzetten naar bytes
        message_bytes = [ord(char) for char in message]

        # cursor naar de juiste positie
        self.arduino.send_sysex(LCD_SET_CURSOR, [0, line])

        # bericht sturen
        self.arduino.send_sysex(LCD_PRINT, message_bytes)

# Dit is een class die doormiddel van de wachtrij theorie de wachttijd berekent
# variabelen bij de init:
# I is de aankomst snelheid
# m is de verwerkings snelheid

# functies:
# add_person() voegt een persoon toe aan de wachtrij
# remove_person() verwijdert een persoon van de wachtrij
# update_wachttijd() berekent de wachttijd door de formule W = T - S
# wachttijd() geeft de wachttijd terug
class QueuingTheory:
    def __init__(self, I, m,):
        self.I = I  
        self.m = m  
        self.people_in_queue = 0
        self.W = 0  
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
        
        g = self.I/self.m  # G = I / M
        

        T = self.people_in_queue / self.I # T = N / I
        S = 1 / self.m # S = 1 / M
        self.W = T - S # W = T - S
        if self.W < 0:
            self.W = 0

    def wachttijd(self):
        return self.W


# Dit is een class die de wachtrij systeem aanstuurt
# variabelen bij de init:
# entry_button_pin is de pin van de entry button
# exit_button_pin is de pin van de exit button
# lcd_display is de lcd scherm
# max_people_in_queue is het maximaal aantal mensen in de wachtrij
# I is de aankomst snelheid
# m is de verwerkings snelheid


# functies:	
# updateDisplay() zorgt ervoor dat de lcd scherm geupdate wordt
# AddPeopleToQueue() voegt een persoon toe aan de wachtrij
# RemovePeopleFromQueue() verwijdert een persoon van de wachtrij
# isEntryButtonPressed() kijkt of de entry button is ingedrukt
# isExitButtonPressed() kijkt of de exit button is ingedrukt
# CheckButtonsAndUpdateQueue() kijkt of de buttons zijn ingedrukt en update de wachtrij

class QueueSystem:
    def __init__(self, entry_button_pin, exit_button_pin, lcd_display, max_people_in_queue,I=1,m=1):
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

    def AddPeopleToQueue(self):
        if self.people_in_queue >= self.max_people_in_queue:
            self.people_in_queue = self.max_people_in_queue
            self.lcd.clear()
            self.lcd.write(0, "Rij is vol!!")
            self.lcd.write(1, "kom later terug")
            print(f"Wachttijd: {self.queuing_theory.wachttijd():.2f} min")

        elif self.people_in_queue >= self.max_people_in_queue * 0.6 and self.people_in_queue < self.max_people_in_queue:
            self.people_in_queue += 1
            self.queuing_theory.add_person()
            self.lcd.clear()
            self.lcd.write(0, f"Mensen in rij {self.people_in_queue}")
            self.lcd.write(1, "Rij is bijna vol!!")
            print(f"Wachttijd: {self.queuing_theory.wachttijd():.2f} min")
            
        else:
            self.people_in_queue += 1
            self.queuing_theory.add_person()
            print(f"Wachttijd: {self.queuing_theory.wachttijd():.2f} min")
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
        entry_pressed = self.isEntryButtonPressed()
        exit_pressed = self.isExitButtonPressed()

        if entry_pressed and exit_pressed:
            # beide knoppen ingedrukt
            return

        if entry_pressed:
            # ingang knop is ingedrukt
            self.AddPeopleToQueue()
            while self.isEntryButtonPressed():
                time.sleep(0.1)

        if exit_pressed:
            # uitgang knop is ingedrukt
            self.RemovePeopleFromQueue()
            while self.isExitButtonPressed():
                time.sleep(0.1)

