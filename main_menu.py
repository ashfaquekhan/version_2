import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import time
import os
import sys
import RPi.GPIO as  GPIO
import shutil

GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP) # SELECT_BUTTON-PIN-31

GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # UP_ARROW_BUTTON-PIN-13

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP) # DOWN_ARROW_BUTTON-PIN-29

GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) # BACK_BUTTON-PIN-15

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # ENTER_BUTTON-PIN-18

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # DELETE_BUTTON-PIN-16


RESET_PIN = 15  # WiringPi pin 15 is GPIO14.
DC_PIN = 16  # WiringPi pin 16 is GPIO15.

spi_bus = 0
spi_device = 0
gpio = gaugette.gpio.GPIO()
spi = gaugette.spi.SPI(spi_bus, spi_device)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
led = gaugette.ssd1306.SSD1306(gpio, spi, reset_pin=RESET_PIN, dc_pin=DC_PIN, rows=32,
                               cols=128)  # Change rows & cols values depending on your display dimensions.
led.begin()
led.clear_display()
led.display()
led.invert_display()
time.sleep(0.5)
led.normal_display()
time.sleep(0.5)


def menu_pos(pos,opr,lim):
    x=pos
    if opr =='d':
        x=x+1
    if x>lim and opr == 'd':
        x=0
    if opr == 'u':
        x=x-1
    if opr == 'u' and x<0:
        x=lim
    return x


h_titl = "PRESS ARROW KEY"
led.draw_text2(0, 15, h_titl, 1)
led.display()
time.sleep(0.2)

def main_menu():
    m_ttl= "MAIN MENU"
    l=0
    while True:
        opt = ["TRANSFER","SAVE","FORMAT","VIEW"]
        up = GPIO.input(27)
        down = GPIO.input(5)
        enter = GPIO.input(24)
        back = GPIO.input(22)
        select = GPIO.input(6)
        len_opt = len(opt)
        len_opt_t = len_opt - 1

        if down == False:
            d='d'
            l=menu_pos(l,d,len_opt_t)
            tex_o = "->"+str(opt[l])
            led.clear_display()
            led.draw_text2(0, 0, m_ttl, 1)
            led.draw_text2(20, 15, tex_o, 1)
            led.display()
            time.sleep(0.2)

        elif  up == False:
            u='u'
            l=menu_pos(l,u,len_opt_t)
            tex_p = "->"+str(opt[l])
            led.clear_display()
            led.draw_text2(0, 0, m_ttl, 1)
            led.draw_text2(20, 15, tex_p, 1)
            led.display()
            time.sleep(0.2)

        elif enter == False:
            if l == 0:
                os.system('python transfer.py')
            if l == 3:
                os.system('python view_menu.py')

while True:
    main_menu()


