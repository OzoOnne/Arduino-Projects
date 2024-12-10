from pyfirmata2 import Arduino, util
import time

board = Arduino('COM5')

while True:
    board.digital[7].write(1)
    time.sleep(1)
    board.digital[7].write(0)
    time.sleep(1)