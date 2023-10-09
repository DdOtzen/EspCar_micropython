from machine import Pin

from lib.carPins import Pins


class Lights:
    class _Light:
        def __init__( self, pins ):
            self.Left  = Pin( pins.Left, Pin.OUT )
            self.Right = Pin( pins.Right, Pin.OUT )

        def on( self ):
            self.Left.on()
            self.Right.on()

        def off( self ):
            self.Left.off()
            self.Right.off()

    def __init__( self ):
        self.Front = self._Light( Pins.Light.Front )
        self.Rear  = self._Light( Pins.Light.Rear )
