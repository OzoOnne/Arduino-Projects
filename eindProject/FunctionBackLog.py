from pyfirmata import Arduino

LCD_PRINT = 0x01
LCD_CLEAR = 0x02
LCD_SET_CURSOR = 0x03

class LCDscherm:
    def __init__(self, arduino):
        self.arduino = arduino
    
    def write(self,line:int,message:str):
        if line > 1: line = 1

        message_bytes = [ord(char) for char in message]

        # Set the cursor to the first position
        
        self.arduino.send_sysex(LCD_SET_CURSOR, [0, line])

        self.arduino.send_sysex(LCD_PRINT, message_bytes)

    # Clear the LCD
    # arduino.send_sysex(LCD_CLEAR, [])