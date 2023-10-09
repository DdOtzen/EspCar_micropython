from time import sleep_ms, sleep
from lib.car import Car

PAUSE_MS = 3_000

def PinTest( pause_secs = 1):
    print( "Front" )
    bil.light.frontLights.on()
    sleep( pause_secs )
    bil.light.frontLights.off()

    print( "Rear" )
    bil.light.rearLights.on()
    sleep( pause_secs )
    bil.light.rearLights.off()

    print( "Left" )
    bil.light.leftLights.on()
    sleep( pause_secs )
    bil.light.leftLights.off()

    print( "Right" )
    bil.light.rightLights.on()
    sleep( pause_secs )
    bil.light.rightLights.off()


print("Just turned on car")
sleep_ms( PAUSE_MS)

print("Initializing car")
bil = Car()
sleep_ms( PAUSE_MS)

print("Pin test")
PinTest(3)

print("Enabling blink relay")
bil.EnableBlinkRelay()
sleep(1)
print("Daytime - no lights")
bil.light.setLights(0)
sleep_ms( PAUSE_MS)

print("Daytime - Turn left")
bil.light.setBlink(2)
sleep_ms( PAUSE_MS)

print("Daytime - Turn right")
bil.light.setBlink(1)
sleep_ms( PAUSE_MS)

print("Daytime - no blink")
bil.light.setBlink(0)
sleep_ms( PAUSE_MS)

print("Nighttime L - low beam")
bil.light.setLights(1)
sleep_ms( PAUSE_MS)

print("Nighttime L - Turn left")
bil.light.setBlink(2)
sleep_ms( PAUSE_MS)

print("Nighttime L - Turn right")
bil.light.setBlink(1)
sleep_ms( PAUSE_MS)

print("Nighttime L - no blink")
bil.light.setBlink(0)
sleep_ms( PAUSE_MS)

print("Nighttime H - high beam")
bil.light.setLights(2)
sleep_ms( PAUSE_MS)

print("Nighttime H - Turn left")
bil.light.setBlink(2)
sleep_ms( PAUSE_MS)

print("Nighttime H - Turn right")
bil.light.setBlink(1)
sleep_ms( PAUSE_MS)

print("Nighttime H - no blink")
bil.light.setBlink(0)
sleep_ms( PAUSE_MS)

