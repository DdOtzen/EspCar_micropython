from time import sleep
from micropython import const
from lib.car import Car



bil = Car()

DEFAULT_SPEED = 30
DEFAULT_STEP_SEC = 1
_TURN_LEFT = const( 0 )
_TURN_RIGHT = const( 1 )
_ROTATE_LEFT = const( 2 )
_ROTATE_RIGHT = const( 3 )


def run_the_tests() :
    try :
        bil.__init__()
        #lights_pin_pair_test()
        bil.EnableBlinkRelay()
        #simple_motor_test( step_secs=1 )
        sqspeed = 40
        square_turn_test( sqspeed, turn_type=_TURN_RIGHT )
        square_turn_test( sqspeed, turn_type=_TURN_LEFT )
        square_turn_test( sqspeed, turn_type=_ROTATE_LEFT )
        square_turn_test( sqspeed, turn_type=_ROTATE_RIGHT )

    finally :
        print( "Shutting down car" )
        bil.sluk()


def square_turn_test( speed=DEFAULT_SPEED, step_secs=DEFAULT_STEP_SEC, repetitions=1, turn_type=_TURN_LEFT ) :
    turn = { _TURN_LEFT    : bil.drejV,
             _TURN_RIGHT   : bil.drejH,
             _ROTATE_LEFT  : bil.roterV,
             _ROTATE_RIGHT : bil.roterH }
    turn_str = { _TURN_LEFT    : "   Dreje Venstre",
                 _TURN_RIGHT   : "   Dreje Højre",
                 _ROTATE_LEFT  : "   Roter Venstre",
                 _ROTATE_RIGHT : "   Roter Højre" }
    if turn_type in [_TURN_LEFT, _ROTATE_LEFT]:
        blinkDir = bil.VENSTRE_BLINK
    else:
        blinkDir = bil.HOEJRE_BLINK

    bil.set_hastighed( speed )
    print( turn_str[turn_type] )
    turn[turn_type]( 90 )

    for rep in range( repetitions ) :
        print(f"Sqaure {rep +1}")

        for side in range(4) :
            print(f"   Side {side} of square")
            bil.frem()
            sleep( step_secs )
            print( turn_str[turn_type] )
            bil.blinklys( blinkDir )
            turn[turn_type]( 90 )
            bil.blinklys( bil.SLUK_LYS )


    print( 'Stop' )
    bil.stop()
    sleep(1)

def basic_turn_test( speed = DEFAULT_SPEED ) :
    bil.set_hastighed( speed )
    for _ in range( 5 ) :
        print( 'drejH' )
        bil.drejH( 90 )

        print( 'drejV' )
        bil.drejV( 90 )

    for _ in range( 5 ) :
        print( 'roterH' )
        bil.roterH( 180 )

        print( 'roterV' )
        bil.roterV( 180 )

    print( 'roterH' )
    bil.roterH( 180 )

    for _ in range( 5 ) :
        print( 'drejH' )
        bil.drejH( 90 )

        print( 'drejV' )
        bil.drejV( 90 )

    print( 'stop' )
    bil.stop()


def ligeudLongTest( speed=DEFAULT_SPEED, step_secs=30 ) :
    bil.set_hastighed( speed )
    bil.frem()
    sleep( step_secs )
    bil.bak()
    sleep( step_secs )
    bil.stop()


def lights_pin_pair_test( step_secs=1 ) :
    print( "Front" )
    bil.light.frontLights.on()
    sleep( step_secs )
    bil.light.frontLights.off()

    print( "Rear" )
    bil.light.rearLights.on()
    sleep( step_secs )
    bil.light.rearLights.off()

    print( "Left" )
    bil.light.leftLights.on()
    sleep( step_secs )
    bil.light.leftLights.off()

    print( "Right" )
    bil.light.rightLights.on()
    sleep( step_secs )
    bil.light.rightLights.off()


def simple_motor_test( speed=DEFAULT_SPEED, step_secs=1 ) :
    bil.set_hastighed( speed )

    print( 'frem' )
    bil.lys( bil.LANGT_LYS )
    bil.frem()
    sleep( step_secs )
    bil.lys( bil.KORT_LYS )

    print( 'bak' )
    bil.bak()
    for _ in range( 10 ) :
        bil.bremselys( bil.TAEND_LYS )
        sleep( step_secs / 20 )
        bil.bremselys( bil.SLUK_LYS )
        sleep( step_secs / 20 )

    print( 'drejH' )
    bil.blinklys( bil.HOEJRE_BLINK )
    bil.drejH()
    sleep( step_secs )
    bil.blinklys( bil.SLUK_LYS )

    print( 'drejV' )
    bil.blinklys( bil.VENSTRE_BLINK )
    bil.drejV()
    sleep( step_secs )
    bil.blinklys( bil.SLUK_LYS )

    print( 'roterH' )
    bil.roterH()
    # Rotating! So front is moving right, rear is moving opposite.
    for _ in range( 10 ) :
        # The scheduler will override this, so if we just keep turning it on we get some blinking effect
        bil.light.lightFR.duty( 1023 )
        bil.light.lightRL.duty( 1023 )
        sleep( 2 * step_secs / 10 )

    print( 'roterV' )
    bil.roterV()
    # Rotating! So front is moving right, rear is moving opposite.
    for _ in range( 10 ) :
        # The scheduler will override this, so if we just keep turning it on we get some blinking effect
        bil.light.lightFL.duty( 1023 )
        bil.light.lightRR.duty( 1023 )
        sleep( 2 * step_secs / 10 )

    print( 'Stop' )
    bil.stop()
    bil.lys( bil.SLUK_LYS )


if __name__ == '__main__' :
        run_the_tests()
