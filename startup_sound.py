from machine import Pin, PWM
import time

# Setup the buzzer on GP15
buzzer = PWM(Pin(15))

def play_tone(frequency, duration):
    """Plays a tone at a given frequency (Hz) for a set duration (seconds)."""
    if frequency == 0:
        buzzer.duty_u16(0)  # Silence
    else:
        buzzer.freq(frequency)
        buzzer.duty_u16(30000)  # Set volume (0-65535)
    time.sleep(duration)
    buzzer.duty_u16(0)  # Turn off the buzzer

def startup_sound():
    """Plays a simple startup jingle."""
    melody = [
        (1000, 0.2),  # (Frequency, Duration)
        (1200, 0.2),
        (1500, 0.2),
        (0, 0.1),  # Silence
        (1800, 0.3),
    ]
    for note in melody:
        play_tone(note[0], note[1])
        time.sleep(0.05)  # Small pause between notes

# Play the startup sound when the script runs
startup_sound()
