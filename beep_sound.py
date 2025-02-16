from machine import Pin, PWM
import time

# Setup the buzzer on GP15
buzzer = PWM(Pin(14))  



def beep(duration=0.2, frequency=10000):
    """Plays a beep for the given duration and frequency."""
    buzzer.freq(frequency)
    buzzer.duty_u16(30000)  # Set volume (0-65535)
    time.sleep(duration)
    buzzer.duty_u16(0)  # Turn off the buzzer


