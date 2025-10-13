from time import sleep, sleep_ms
from lib.car import Car

bil = Car()

bil.set_hastighed( 40 )

# Kør frem til Kasse
bil.frem()
while bil.Distance() < 200 :
    pass

# Stop og drej
bil.stop()
sleep_ms(100)
bil.roterV(90)
sleep_ms(100)

#Kør mos væg
bil.frem()
while bil.Distance() < 452 :
    pass

# Stop og drej
bil.stop()
sleep_ms(100)
bil.roterH(90)
sleep_ms(100)

# Kør mod mål
while bil.Distance() > 200 :
    pass
bil.stop()

bil.sluk()
