from time import sleep, sleep_ms
from lib.car import Car

bil = Car()


for s in range( 0, 101, 10): 
    bil.set_hastighed( s )
    bil.bak()
    sleep(1)
    bil.stop()
    bil.frem()
    sleep(1)
    bil.stop()

bil.sluk()