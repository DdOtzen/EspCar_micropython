from machine import Encoder, Pin, freq, Timer
import esp32
from time import sleep
from lib.car import Car


enc = Encoder(0, phase_a=Pin(36, mode=Pin.IN), phase_b=Pin(39, mode=Pin.IN), filter_ns=0, x124=1)
tim1 = Timer(1)
bil = Car()
speed = 0

print(f"CPU speed: {freq()}")
def tick(timer):
    global enc
    #print(f"CPU temp: { (esp32.raw_temperature() - 32) * 0.5555556 } C")
    #print(f"The filter value: {enc.filter_ns()}")
    print("enc:", enc.value(), "speed ‰:", speed*10, 3000)
    
n = 0
def irq_handler1(self):
    global n
    n -= 1
    #print('irq_handler1()', self.id(), self.value(), n)

def irq_handler2(self):
    global n
    n += 1
    print('irq_handler2()', self.id(), self.value(), n)


try:
    tim1.init(freq=1, mode=Timer.PERIODIC, callback=tick )

    enc.pause()
    enc.irq(irq_handler1, Encoder.IRQ_MATCH1, value=100)  # set irq handler
    enc.resume()
    
    def fb(bil):
        #print('frem')
        bil.frem()
        sleep(2)
        
        #print('bak')
        bil.bak()
        sleep(2)

    for s in range(0, 101, 20):
        speed = s
        bil.set_hastighed(s)
        fb(bil)
    
    bil.set_hastighed(0)
    bil.frem()
    sleep(2)
    bil.coast()
    
    while True:
        pass

finally:
    enc.deinit()  # free the input pins and encoder.
    tim1.deinit()
    bil.coast()
    print("shut down")
    