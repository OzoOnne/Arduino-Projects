from pyfirmata2 import Arduino, util
import time

# Stel de board in
board = Arduino('COM5')  # Vervang met de juiste poort, zoals 'COM3' of '/dev/ttyUSB0'

# Definieer de pinnen
button_pin = 12
led_pin = 7

# Wacht even om ervoor te zorgen dat de communicatie goed werkt
time.sleep(2)

# Zet de pinmodi (met integer waarden)
board.digital[button_pin].mode = 2  # Gebruik 2 voor INPUT_PULLUP
board.digital[led_pin].mode = 1  # Gebruik 1 voor OUTPUT

# Wacht nog even
time.sleep(1)

# Button control functie
def button_control_led(board, button_pin, led_pin):
    while True:
        # Lees de staat van de knop (actief laag, dus 0 betekent ingedrukt)
        try:
            button_state = board.digital[button_pin].read()
            if button_state is not None:
                if button_state == 0:  # Knop ingedrukt (actief laag)
                    board.digital[led_pin].write(1)  # Zet LED aan
                else:
                    board.digital[led_pin].write(0)  # Zet LED uit
            else:
                print("Knopstatus is None - controleer de verbindingen")
        except Exception as e:
            print(f"Fout bij het lezen van de knop: {e}")

        # Kleine vertraging om de leesfrequentie te verminderen
        time.sleep(0.1)

# Start de knop controle
button_control_led(board, button_pin, led_pin)
