from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms


LED_PIN = 19
LED_COUNT = 12

FRONT = range(0, 6)
REAR = range(6, 12)
LEFT = (0, 1, 2, 9, 10, 11)
RIGHT = (3, 4, 5, 6, 7, 8)

OFF = (0, 0, 0)
WHITE = (100, 100, 100)
RED = (100, 0, 0)
AMBER = (100, 35, 0)

pixels = NeoPixel(Pin(LED_PIN), LED_COUNT)


def base_color(index):
    return WHITE if index in FRONT else RED


def restore_base():
    for index in range(LED_COUNT):
        pixels[index] = base_color(index)
    pixels.write()


def color_wipe():
    pixels.fill(OFF)
    pixels.write()
    for index in range(LED_COUNT):
        pixels[index] = base_color(index)
        pixels.write()
        sleep_ms(90)
    sleep_ms(350)


def turn_signal(side):
    for _ in range(3):
        restore_base()
        for index in side:
            pixels[index] = AMBER
        pixels.write()
        sleep_ms(280)
        restore_base()
        sleep_ms(220)


def brake_pulse():
    for brightness in (30, 70, 100, 70, 30, 0):
        red = (brightness, 0, 0)
        for index in REAR:
            pixels[index] = red
        pixels.write()
        sleep_ms(70)
    restore_base()
    sleep_ms(300)


def wheel(position):
    position = 255 - position
    if position < 85:
        return (255 - position * 3, 0, position * 3)
    if position < 170:
        position -= 85
        return (0, position * 3, 255 - position * 3)
    position -= 170
    return (position * 3, 255 - position * 3, 0)


def rainbow_scan():
    for offset in range(LED_COUNT * 3):
        for index in range(LED_COUNT):
            pixels[index] = wheel((index * 256 // LED_COUNT + offset * 8) & 255)
        pixels.write()
        sleep_ms(35)
    restore_base()


def run_show():
    while True:
        color_wipe()
        turn_signal(LEFT)
        turn_signal(RIGHT)
        brake_pulse()
        rainbow_scan()


try:
    run_show()
except KeyboardInterrupt:
    pass
finally:
    pixels.fill(OFF)
    pixels.write()