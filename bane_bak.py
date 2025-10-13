from time import sleep, sleep_ms
from micropython import const
from lib.car import Car



bil = Car()

def FremUntil( dist ):
    bil.langLys()
    bil.frem()
    while bil.Distance() > dist  :
        pass
    bil.stop()
    sleep_ms(100)
    bil.kortLys()
    

def BakUntil( dist ):
    bil.bremselys(1)
    bil.bak()
    while bil.Distance() < dist :
        pass
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

# Frem til kasse.
FremUntil( 300 )

#Drej og bak
RotV( 85 )

BakUntil( 900 )

RotH( 85 )

Afslut()

bil.sluk()
