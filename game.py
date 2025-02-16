from machine import Pin, I2C, PWM
import time
import random
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

# LCD setup (I2C Address 0x27)
I2C_ADDR = 0x27
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Button setup
btn_left = Pin(14, Pin.IN, Pin.PULL_UP)
btn_right = Pin(13, Pin.IN, Pin.PULL_UP)

# Buzzer setup
buzzer = PWM(Pin(15))

# Game variables
player_pos = 7  # Player starts in the middle
obstacle_pos = random.randint(0, 15)
score = 0



def display_game()
    Updates the LCD with the game state.
    lcd.clear()
    # Top row with obstacle
    top_row = [ ]  16
    top_row[obstacle_pos] = X
    lcd.move_to(0, 0)
    lcd.putstr(.join(top_row))
    
    # Bottom row with player
    bottom_row = [ ]  16
    bottom_row[player_pos] = P
    lcd.move_to(0, 1)
    lcd.putstr(.join(bottom_row))

def move_player()
    Moves the player left or right based on button input.
    global player_pos
    if not btn_left.value() and player_pos  0
        player_pos -= 1
    if not btn_right.value() and player_pos  15
        player_pos += 1

# Game loop
lcd.clear()
lcd.putstr(Dodge the X!)
time.sleep(1)

while True
    move_player()
    display_game()
    time.sleep(0.5)

    # Check collision
    if obstacle_pos == player_pos
        lcd.clear()
        lcd.putstr(Game Over!)
        lcd.move_to(0, 1)
        lcd.putstr(fScore {score})
        break

    # Move obstacle
    obstacle_pos = random.randint(0, 15)
    score += 1

