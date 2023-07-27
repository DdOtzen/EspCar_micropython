from machine import Pin
try:
    from time import sleep_ms
except ImportError:
    from time import sleep
    def sleep_ms( ms ):
        sleep( ms / 1000 )

from lib.car import Car
bil = Car()


class Encoder:
    def __init__(self, pin_x, pin_y, scale=1):
        self.scale = scale
        self.pin_x = pin_x
        self.pin_y = pin_y
        self._pos = 0
        try:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback, hard=True)
            self.y_interrupt = pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback, hard=True)
        except TypeError:
            self.x_interrupt = pin_x.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.x_callback)
            self.y_interrupt = pin_y.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=self.y_callback)

    def x_callback(self, pin_x):
        forward = pin_x() ^ self.pin_y()
        self._pos += 1 if forward else -1

    def y_callback(self, pin_y):
        forward = self.pin_x() ^ pin_y() ^ 1
        self._pos += 1 if forward else -1

    def position(self, value=None):
        if value is not None:
            self._pos = round(value / self.scale)
        return self._pos * self.scale

a1=Pin( 35, Pin.IN )
a2=Pin( 34, Pin.IN )

enc = Encoder( a1, a2 )



while True:
    print(enc.position()/832)
    sleep(1)
