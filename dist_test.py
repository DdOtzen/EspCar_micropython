from time import sleep, sleep_ms
from micropython import const
from lib.car import Car



bil = Car()

mdist = 0
def FremUntil( dist ):
    bil.langLys()
    bil.frem()
    while bil.Distance() > dist  :
        pass
    bil.stop()
    sleep_ms(100)
    bil.kortLys()
    

def BakUntil( dist ):
    global mdist
    bil.bremselys(1)
    bil.bak()
    while bil.Distance() < dist:
        _mdist = bil.Distance()
        if _mdist < dist:
            mdist=_mdist
    bil.bremselys(0)
    bil.stop()
    sleep_ms(100)
    

def RotV( deg ):
    bil.blinklys(bil.VENSTRE)
    sleep_ms(100)
    bil.roterV( deg )
    sleep_ms(100)
    bil.blinklys(bil.SLUK)

def RotH( deg ):
    bil.blinklys(bil.HOEJRE)
    bil.roterH( deg )
    sleep_ms(100)
    bil.blinklys(bil.SLUK)

def Afslut():
    bil.frem()
    sleep_ms(3000)
    bil.stop()
    sleep_ms(100)
    bil.roterH(180)
    bil.roterH(180)
    bil.roterV(180)
    bil.roterV(180)

print("Enabling blink relay")
bil.EnableBlinkRelay()
bil.set_hastighed( 30 )


#BakUntil( 8000 )
#fdist = bil.Distance() 
while True:
#    print("pre final distance", mdist)
#    print("final distance", fdist)
    print("distance:", bil.Distance())
    sleep_ms(500)
bil.sluk()

