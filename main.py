import utime
import machine
from machine import I2C, Pin
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
import startup_sound

I2C_ADDR = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

# Initialize I2C and LCD
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Buttons
button = Pin(14, Pin.IN, Pin.PULL_UP)
select_button = Pin(13, Pin.IN, Pin.PULL_UP)

# Menu options and corresponding Python files
menu_items = [
    ("Dodge the x", "game.py"),
    ("Apps", "apps.py"),
    ("Battery", "battery.py"),
    ("Time", "time_display.py"),
    ("dino game", "dino game.py"),
]
selected = 0  # Start at the first item

def beep():  # Sound function
    import beep

def update_lcd():
    """Updates the LCD display with the current selection."""
    lcd.clear()
    lcd.move_to(3, 0)
    lcd.putstr(menu_items[selected][0])  # Display menu name
    import beep

# Initial display
update_lcd()

while True:
    if button.value() == 0:  # When button is pressed
        utime.sleep(0.2)  # Debounce delay
        selected = (selected + 1) % len(menu_items)  # Cycle through menu
        update_lcd()  # Update display
        beep()
    if select_button.value() == 0:  # When select_button is pressed
        utime.sleep(0.2)  # Debounce delay
        script = menu_items[selected][1]  # Get corresponding Python file
        
        try:
            exec(open(script).read())  # Run the Python file
        except Exception as e:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("Error opening:")
            lcd.move_to(0, 1)
            lcd.putstr(script)
            print("Error:", e)  # Print error for debugging
        utime.sleep(1)  # Short delay before returning to menu
        
    utime.sleep(0.05)  # Small delay to reduce CPU usage


