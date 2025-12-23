import time
from display import OLEDDisplay
from ui import OLEDUI

display = OLEDDisplay()
ui = OLEDUI(display)

ui.draw()

time.sleep(2)
ui.update("camera", "OK")

time.sleep(2)
ui.update("quality", "GOOD")

time.sleep(2)
ui.update("pc", "ON")

time.sleep(2)
ui.update("robot", "MOVING")

while True:
    time.sleep(1)
