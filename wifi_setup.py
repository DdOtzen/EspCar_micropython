import network
from time import ticks_ms, ticks_diff

try :
    import _secrets
except ImportError :
    print( "You need to create the _secrets.py file, see the _secrets.py.template file." )
    raise SystemExit( "Missing the _secret.py file." )

wifi = network.WLAN( network.STA_IF )

def start_wifi():
    try:
        print( "Connecting to WiFi..." )
        
        wifi.active( True )
        wifi.connect( _secrets.WIFI_SSID, _secrets.WIFI_PASS )
        start_tick = ticks_ms()  # get millisecond counter
        while not wifi.isconnected() :
            waitTime = ticks_diff( ticks_ms(), start_tick)
            if waitTime > 5000:
                break
        
        print( 'IP:', wifi.ifconfig()[0] )
    except:
        network.WLAN(network.STA_IF).disconnect()
        raise

def stop_wifi() :
    network.WLAN( network.STA_IF ).disconnect()
