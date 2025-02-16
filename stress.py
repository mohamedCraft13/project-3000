from machine import Pin, I2C
import time
import math
import gc
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# LCD setup (I2C Address: 0x27)
I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# GPIO stress test setup
pins = [Pin(i, Pin.OUT) for i in range(2, 15)]  # Use GPIO 2-14
restart_btn = Pin(13, Pin.IN, Pin.PULL_UP)  # GP14 as restart button
# Store the highest score
best_score = 0

def display_message(line1, line2=""):
    """Updates the LCD with the given messages."""
    lcd.clear()
    lcd.putstr(line1)
    lcd.move_to(0, 1)
    lcd.putstr(line2)

def cpu_stress():
    """Performs heavy calculations to max out the CPU."""
    display_message("CPU Test:", "Running...")
    start = time.ticks_ms()
    for _ in range(50000):
        math.sqrt(12345678)
        math.sin(3.14159)
        math.log(1234)
    end = time.ticks_ms()
    cpu_time = end - start
    display_message("CPU Done!", f"Time: {cpu_time}ms")
    time.sleep(2)
    
    # Score based on CPU speed (lower time = higher score)
    return max(0, 1000 - cpu_time)

def memory_stress():
    """Allocates large lists to fill RAM."""
    display_message("Memory Test:", "Allocating...")
    try:
        big_list = [i for i in range(10000)]
        big_list = [big_list] * 10
        display_message("Memory OK!", "Test Passed")
        mem_score = 500  # Max memory score if successful
    except MemoryError:
        display_message("Memory Error!", "RAM Full")
        mem_score = 100  # Lower score if RAM is full
    gc.collect()
    time.sleep(2)
    
    return mem_score

def gpio_stress():
    """Toggles GPIO pins as fast as possible."""
    display_message("GPIO Test:", "Toggling...")
    start = time.ticks_ms()
    for _ in range(10000):
        for pin in pins:
            pin.value(1)
        for pin in pins:
            pin.value(0)
    end = time.ticks_ms()
    gpio_time = end - start
    display_message("GPIO Done!", f"Time: {gpio_time}ms")
    time.sleep(2)

    # Score based on GPIO speed (lower time = higher score)
    return max(0, 1000 - gpio_time)

def full_stress_test():
    """Runs all stress tests and calculates a final score."""
    global best_score
    display_message("Starting Test", "Please wait...")
    time.sleep(2)

    cpu_score = cpu_stress()
    mem_score = memory_stress()
    gpio_score = gpio_stress()

    # Calculate total score
    total_score = cpu_score + mem_score + gpio_score
    if total_score > best_score:
        best_score = total_score  # Update best score

    # Show final score
    display_message("Score:", f"{total_score} pts")
    time.sleep(2)
    display_message("Best Score:", f"{best_score} pts")
    time.sleep(3)

# Run the stress test once
full_stress_test()

# Wait for the restart button press to restart the test
while True:
    if not restart_btn.value():  # If button is pressed
        display_message("Restarting...", "")
        time.sleep(1)
        full_stress_test()
    else:
        break

