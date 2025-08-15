from time import sleep_ms
from lib.car import Car

print("Starter bil")
bil = Car()
bil.name = "Jens' bil"
bil.EnableBlinkRelay()

lodo = 0
hodo = 0


#find venstre kant
bil.blinklys(bil.VENSTRE)
bil.set_hastighed( 20 )
bil.roterV(90)
bil.blinklys(bil.SLUK)

bil.set_hastighed( 50 )
bil.frem()
while (hodo < 90):
    hodo += 1
    sleep_ms(10)
    
bil.blinklys(bil.HOEJRE)
bil.set_hastighed( 20 )
bil.roterH(90)
bil.blinklys(bil.SLUK)
    
hodo = 0
bil.set_hastighed( 50 )
bil.frem()  
while (bil.Distance() > 300) and (lodo < 500):
    lodo += 1
    sleep_ms(10)

hodo = 0
if (lodo < 500):
    i = 0
    while (bil.Distance() < 150):
        bil.blinklys(bil.HOEJRE)
        bil.set_hastighed( 20 )
        bil.roterH(90)
        bil.blinklys(bil.SLUK)
        bil.set_hastighed( 50 )
        bil.frem()
        sleep_ms(2000)
        bil.stop()
#        while (i < 5):
#            i += 1
#            sleep_ms(10)
        bil.blinklys(bil.VENSTRE)
        bil.set_hastighed( 20 )
        bil.roterV(90)
        bil.blinklys(bil.SLUK)
        
    bil.lys.kortLys()
    
    bil.set_hastighed( 50 )
    bil.frem()  
while (bil.Distance() > 300) and (lodo < 500):
    lodo += 1
    sleep_ms(10)
    bil.set_hastighed( 20 )
    bil.roterV(90)
    bil.blinklys(bil.SLUK)
    hodo += 50
else :
    bil.blinklys(bil.HOEJRE)
    bil.set_hastighed( 20 )
    bil.roterH(90)
    bil.blinklys(bil.SLUK)
    bil.set_hastighed( 50 )
    bil.frem()
    while (hodo < 150):
        hodo += 1
        sleep_ms(10)
        

print("kørt afstand: ",lodo)
bil.sluk()

