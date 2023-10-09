try:
    from micropython import const
except ImportError:
    # we get here if running cPython on host.
    print( 'Using pseudo const' )
    def const( x ):
        return x


class Pins:

    class Motor:
        class Left:
            Forward : const
            Reverse : const
            Speed   : const
            enc_1   : const
            enc_2   : const
        class Right:
            Forward : const
            Reverse : const
            Speed   : const
            enc_1   : const
            enc_2   : const

        # Dummy attribute to help with simpler typehints.
        LR = Left

    # Basic Python syntax do allow this to be declared directly in the class defenitions above, but the special
    # micropython 'const' gets confused and can't destuinguish between variables of same name in differen class scopes.
    # Thus, decleration is done here, with the full path to variable in the assigments.
    Motor.Left.Speed    = const(25)
    Motor.Left.Forward  = const(32)
    Motor.Left.Reverse  = const(33)
    Motor.Left.enc_1   = const(36)
    Motor.Left.enc_2   = const(39)

    # Right motor has in and enc pins swapped, pcb design forgot the motors is turned 180 deg from each other.
    Motor.Right.Speed   = const(14)
    Motor.Right.Forward = const(27)
    Motor.Right.Reverse = const(26)
    Motor.Right.enc_1    = const(35)
    Motor.Right.enc_2    = const(34)

    class Light:
        class Front:
            Left  : const
            Right : const
        class Rear:
            Left  : const
            Right : const
        # Dummy attribute to help with simpler typehints.
        FR = Front

    Light.Front.Left  = const( 18 )
    Light.Front.Right = const( 19 )
    Light.Rear.Left   = const( 15 )
    Light.Rear.Right  = const( 4 )

    class I2C:
        SCL = const(22)
        SDA = const(21)


if __name__ == '__main__':
    #print( dir(pin))
    #print( pin.RightMotor.Forward )
    print( f'{Pins.Motor.Right.Forward=}' )
    print( f'{Pins.Motor.Right.Reverse=}' )
    print( f'{Pins.Motor.Right.Speed=}' )
    print( f'{Pins.Motor.Left.Forward=}' )
    print( f'{Pins.Motor.Left.Reverse=}' )
    print( f'{Pins.Motor.Left.Speed=}' )
    print( f'{Pins.Light.Front.Right=}' )
    print( f'{Pins.Light.Front.Left=}' )
    print( f'{Pins.Light.Rear.Right=}' )
    print( f'{Pins.Light.Rear.Left=}' )

    #pin = Pins()
