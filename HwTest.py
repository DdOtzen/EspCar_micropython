from machine import Pin, I2C, Encoder
from time import sleep_ms, sleep
from lib.lights import Lights
from lib.carPins import Pins
from lib.mpu6500 import MPU6500, SF_G, SF_DEG_S
from lib.vl53l0x import VL53L0X
from lib.motor import Motor


light = Lights()
sleep(1) # I do not know why this is needed


# Show is alive
light.lightFL.duty_u16(65535)
sleep_ms( 500 )
light.lightFR.duty_u16(65535)
sleep_ms( 500 )
light.lightRR.duty_u16(65535)
sleep_ms( 500 )
light.lightRL.duty_u16(65535)
sleep_ms( 500 )
light.sluk()
sleep_ms( 1000 )


# Test i2c
light.lightFL.duty_u16(65535)
light.lightFR.duty_u16(65535)
light.lightRR.duty_u16(65535)
light.lightRL.duty_u16(65535)
i2c = I2C(0, sda=Pin(Pins.I2C.SDA), scl=Pin(Pins.I2C.SCL))
sleep_ms( 500 )
light.sluk()
sleep_ms( 1000 )

# Test Distance module - only if present on i2c
light.lightFL.duty_u16(65535)
light.lightFR.duty_u16(65535)
tofSensor = VL53L0X(i2c)
sleep_ms( 500 )
light.sluk()
sleep_ms( 1000 )

# Test accelerometer+gyroscope  - only if present on i2c
light.lightRL.duty_u16(65535)
light.lightRR.duty_u16(65535)
MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sleep_ms( 500 )
light.sluk()
sleep_ms( 1000 )

# Test left motor with encoder
leftMotor = Motor(Pins.Motor.Left)
leftMotorEnc = Encoder(0, leftMotor.encPinB, leftMotor.encPinA)
sleep(1) # I do not know why this is needed
leftMotor.SetPower(25)
light.lightFL.duty_u16(65535)
leftMotor.forward()
pulses = leftMotorEnc.value(0)
while( leftMotorEnc.value() < 20 ):
    pass
leftMotor.Stop()
light.sluk()
sleep_ms(100)
light.lightRL.duty_u16(65535)
leftMotor.reverse()
pulses = leftMotorEnc.value(0)
while( leftMotorEnc.value() > -20 ):
    pass
leftMotor.Stop()
light.sluk()

#Test right motor with encoder
rightMotor = Motor(Pins.Motor.Right)
rightMotorEnc = Encoder(1, rightMotor.encPinB, rightMotor.encPinA)
sleep(1) # I do not know why this is needed
rightMotor.SetPower(25)
light.lightFR.duty_u16(65535)
rightMotor.forward()
pulses = rightMotorEnc.value(0)
while( rightMotorEnc.value() < 20 ):
    pass
rightMotor.Stop()
light.sluk()
sleep_ms(100)
light.lightRR.duty_u16(65535)
rightMotor.reverse()
pulses = rightMotorEnc.value(0)
while( rightMotorEnc.value() > -20 ):
    pass
rightMotor.Stop()
light.sluk()


