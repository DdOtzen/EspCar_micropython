from time import sleep_ms
from lib.car import Car

print("Starter bil")
bil = Car()
bil.name = "Cool Cat"

bil.set_hastighed( 50 )
bil.frem()

bil.sluk()
