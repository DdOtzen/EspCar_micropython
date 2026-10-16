from time import sleep_ms, sleep
from lib.car import Car

SIMPLE_PAUSE_MS = 1_000
PAUSE_MS = 3_000

def PinTest(pause_secs=1):
    print("Front")
    bil.forlygter.on()
    sleep(pause_secs)
    bil.forlygter.off()

    print("Rear")
    bil.baglygter.on()
    sleep(pause_secs)
    bil.baglygter.off()

    print("Left")
    bil.venstreLys.on()
    sleep(pause_secs)
    bil.venstreLys.off()

    print("Right")
    bil.højreLys.on()
    sleep(pause_secs)
    bil.højreLys.off()


def BlinkTest():
    print("Enabling blink relay")
    bil.EnableBlinkRelay()
    sleep(1)
    print("Daytime - no lights")
    bil.lys.sluk()
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Daytime - Turn left")
    bil.blinklys(bil.VENSTRE)
    sleep_ms(PAUSE_MS)

    print("Daytime - Turn right")
    bil.blinklys(bil.HOEJRE)
    sleep_ms(PAUSE_MS)

    print("Daytime - no blink")
    bil.blinklys(bil.SLUK)
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Nighttime L - low beam")
    bil.lys.kortLys()
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Nighttime L - Turn left")
    bil.blinklys(bil.VENSTRE)
    sleep_ms(PAUSE_MS)

    print("Nighttime L - Turn right")
    bil.blinklys(bil.HOEJRE)
    sleep_ms(PAUSE_MS)

    print("Nighttime L - no blink")
    bil.blinklys(bil.SLUK)
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Nighttime H - high beam")
    bil.lys.langLys()
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Nighttime H - Turn left")
    bil.blinklys(bil.VENSTRE)
    sleep_ms(PAUSE_MS)

    print("Nighttime H - Turn right")
    bil.blinklys(bil.HOEJRE)
    sleep_ms(PAUSE_MS)

    print("Nighttime H - no blink")
    bil.blinklys(bil.SLUK)
    sleep_ms(SIMPLE_PAUSE_MS)


def BrakeTest():
    print("Brake lights - normal rear brightness")
    bil.lys.kortLys()
    sleep_ms(SIMPLE_PAUSE_MS)

    print("Brake lights - brighter red")
    bil.bremselys(bil.lys.ON)
    sleep_ms(SIMPLE_PAUSE_MS)
    bil.bremselys(bil.lys.OFF)
    sleep_ms(SIMPLE_PAUSE_MS)


print("Initializing car")
bil = Car()

try:
    print("Pin test")
    PinTest(1)

    print("Brake test")
    BrakeTest()

    print("Blink test")
    BlinkTest()
finally:
    print("Test complete - lights off")
    bil.blinklys(bil.SLUK)
    bil.lys.sluk()

#print("Shutting down car")
#bil.sluk()
