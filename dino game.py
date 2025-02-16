from machine import Pin, I2C
import time
import random
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# LCD setup (I2C Address: 0x27)
I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Button setup for jump (GP14)
btn_jump = Pin(14, Pin.IN, Pin.PULL_UP)
# (Note: GP13 is not used since we no longer restart on button press)

# Game variables
dino_pos = 1   # 1 = ground, 0 = jump
cactus_pos = 15  # Cactus starts on the right edge
score = 0
jumping = False
last_jump_time = 0

def display_game():
    """Updates the LCD with the game state."""
    # Top row: Display score and, if in the air, the dino
    top_row = f"Score:{score:<3}"
    top_display = [" "] * 16
    for i, char in enumerate(top_row):
        top_display[i] = char
    if dino_pos == 0:
        top_display[6] = "D"  # Dino in the air at column 6
    lcd.move_to(0, 0)
    lcd.putstr("".join(top_display))

    # Bottom row: Display ground with dino and cactus
    bottom_row = [" "] * 16
    if dino_pos == 1:
        bottom_row[6] = "D"  # Dino on the ground at column 6
    bottom_row[cactus_pos] = "X"  # Cactus
    lcd.move_to(0, 1)
    lcd.putstr("".join(bottom_row))

def jump():
    """Triggers the dino jump if the jump button is pressed."""
    global dino_pos, jumping, last_jump_time
    if not btn_jump.value() and not jumping:
        jumping = True
        dino_pos = 0
        last_jump_time = time.ticks_ms()

def update_jump():
    """Ends the jump after a short duration."""
    global dino_pos, jumping
    if jumping and time.ticks_diff(time.ticks_ms(), last_jump_time) > 300:
        dino_pos = 1
        jumping = False

# Start game screen
lcd.clear()
lcd.putstr("Google Dino Game")
time.sleep(1)
lcd.clear()

# Main game loop
while True:
    jump()         # Check for jump input
    update_jump()  # Update jump state

    # Move the cactus
    cactus_pos -= 1
    if cactus_pos < 0:
        cactus_pos = 15  # Reset cactus to the right edge
        score += 1       # Increase score

    # Check for collision: if cactus is at column 6 and dino is on the ground
    if cactus_pos == 6 and dino_pos == 1:
        lcd.clear()
        lcd.putstr("Game Over!")
        lcd.move_to(0, 1)
        lcd.putstr(f"Score: {score}")
        break  # Exit the game loop

    display_game()
    time.sleep(0.1)  # Fast game loop for responsiveness
