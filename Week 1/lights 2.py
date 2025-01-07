import time
from pyfirmata import Arduino, util

# Verbinden met de Arduino (pas de poort aan naar jouw systeem)
board = Arduino('COM5')  # Voor Windows, of '/dev/ttyACM0' voor Linux

# Stel de digitale pin in voor de DHT11 (bijvoorbeeld D2)
dht_pin = board.get_pin('d:2:i')  # 'd:2:i' betekent digitale pin 2, ingang (input)

# Functie om de DHT11 sensor aan te sturen en de gegevens te lezen
def read_dht11():
    # Zet de pin eerst als OUTPUT voor het verzenden van een signaal naar de DHT11
    board.digital[2].mode = 1  # Zet pin D2 naar OUTPUT

    # Het DHT11-signaal vereist een specifieke tijdsinstelling
    # Start met het verzenden van een signaal om de sensor te activeren
    board.digital[2].write(0)  # Zet de pin laag
    time.sleep(0.018)  # 18 milliseconden wachten

    board.digital[2].write(1)  # Zet de pin hoog
    time.sleep(0.00002)  # 20 microseconden wachten

    board.digital[2].write(0)  # Zet de pin weer laag voor de sensor om te reageren

    # Zet de pin nu terug naar INPUT om de data van de sensor te lezen
    board.digital[2].mode = 0  # Zet pin D2 naar INPUT

    # Nu gaan we de respons van de sensor lezen:
    # We lezen 40 bits die de sensor zal verzenden
    bits = []
    for i in range(40):
        start_time = time.time()

        # Wacht tot de pin hoog wordt, en meet de tijd
        while board.digital[2].read() == 0:
            pass

        pulse_time = time.time() - start_time  # De tijd hoe lang de pin hoog blijft

        # Als de tijd langer is dan een bepaalde drempel, beschouwen we dit als een logische 1
        if pulse_time > 0.00005:
            bits.append(1)
        else:
            bits.append(0)

    # Nu moeten we de 40 bits omzetten naar de daadwerkelijke temperatuur- en luchtvochtigheidswaarden
    humidity = 0
    temperature = 0

    # De eerste 8 bits zijn de luchtvochtigheid (hoge byte en lage byte)
    for i in range(8):
        humidity = humidity + (bits[i] << (7 - i))

    # De volgende 8 bits zijn de temperatuur (hoge byte en lage byte)
    for i in range(8, 16):
        temperature = temperature + (bits[i] << (15 - i))

    # Het resultaat bevat ook een checkbyte voor de integriteit van de data
    checksum = 0
    for i in range(32, 40):
        checksum = checksum + (bits[i] << (39 - i))

    # Controleer of de som van de eerste 8 bits gelijk is aan de checksum
    if humidity + temperature == checksum:
        print(f"Luchtvochtigheid: {humidity}%")
        print(f"Temperatuur: {temperature}°C")
    else:
        print("Fout bij het lezen van de DHT11 sensor!")

# Start de meting
try:
    while True:
        read_dht11()  # Lees de DHT11 gegevens
        time.sleep(2)  # Wacht 2 seconden voordat je opnieuw leest

except KeyboardInterrupt:
    print("Programma gestopt door gebruiker.")
finally:
    board.exit()  # Stop de verbinding met de Arduino
    print("Arduino-verbinding afgesloten.")
