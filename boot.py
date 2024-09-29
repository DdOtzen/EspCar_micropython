# This file is executed on every boot (including wake-boot from deepsleep)
# from wifi_setup import start_wifi, wifi, stop_wifi
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
# start_wifi()
from lib.car import Car
import time


try:
    import AutoRun
    print( "Shutting down car" )
    Car.sluk()
except ImportError as e:
    if "'AutoRun'" not in e.value:
        Car.Emergency_shutdown()
        raise
    # else just ignore it
except KeyboardInterrupt:
    raise
except:
    Car.Emergency_shutdown()
    raise
