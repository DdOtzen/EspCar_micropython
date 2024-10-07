from time import sleep_ms
from lib.car import Car


bil = Car()

bil.EnableBlinkRelay()

while True:
    if bil.Distance() > 400:
        bil.lys.langLys()
        bil.blinklys( bil.SLUK)
    elif bil.Distance() > 300:
        bil.lys.sluk()
        bil.bremselys(0)
        bil.blinklys( bil.HOEJRE )
    elif bil.Distance() > 200:
        bil.lys.sluk()
        bil.bremselys(0)
        bil.blinklys( bil.VENSTRE )
    else:
        bil.blinklys( bil.SLUK)
        bil.lys.sluk()
        bil.bremselys(1)
        
    sleep_ms(300)
    print(bil.distance)
    
