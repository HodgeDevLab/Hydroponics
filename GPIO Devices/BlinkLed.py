from gpiozero import LED
from time import sleep
from pin_config import *

try:
    while True:
        for GPIO_PIN in GPIO_ALL:
            # Set up the LED pin number
            led = LED(GPIO_PIN)  # Change to the pin you're using
            led.on()  # Turn on LED
            sleep(0.1)  # Wait for 1 second
            led.off()  # Turn off LED
            sleep(0.1)  # Wait for 1 second

except KeyboardInterrupt:
    pass
