import sys
from time import sleep_ms
from machine import Encoder

from lib.carPins import Pins
from lib.motor import Motor


TEST_POWER = 25
PULSE_MS = 250
SETTLE_MS = 100


def count_phase_changes(motor):
    previous_a = motor.encPinA.value()
    previous_b = motor.encPinB.value()
    changes_a = 0
    changes_b = 0
    for _ in range(PULSE_MS):
        sleep_ms(1)
        current_a = motor.encPinA.value()
        current_b = motor.encPinB.value()
        if current_a != previous_a:
            changes_a += 1
        if current_b != previous_b:
            changes_b += 1
        previous_a = current_a
        previous_b = current_b
    return changes_a, changes_b


motors = []
encoders = []

try:
    for name, pins, encoder_id in (
        ("LEFT", Pins.Motor.Left, 0),
        ("RIGHT", Pins.Motor.Right, 1),
    ):
        motor = Motor(pins)
        motors.append((name, motor))
        motor.SetPower(0)
        motor.Stop()
        encoder = Encoder(encoder_id, motor.encPinB, motor.encPinA)
        encoders.append((name, motor, encoder, encoder_id))

    print("MicroPython", sys.version)
    print("MOTOR_ENCODER_PREFLIGHT_OK")

    for name, motor, encoder, encoder_id in encoders:
        start = encoder.value()

        motor.SetPower(TEST_POWER)
        motor.forward()
        phase_changes_forward = count_phase_changes(motor)
        motor.SetPower(0)
        motor.Stop()
        sleep_ms(SETTLE_MS)
        forward = encoder.value()

        motor.SetPower(TEST_POWER)
        motor.reverse()
        phase_changes_reverse = count_phase_changes(motor)
        motor.SetPower(0)
        motor.Stop()
        sleep_ms(SETTLE_MS)
        reverse = encoder.value()

        print(
            "RESULT",
            name,
            "PCNT",
            encoder_id,
            "start",
            start,
            "forward",
            forward,
            "reverse",
            reverse,
            "forward_delta",
            forward - start,
            "reverse_delta",
            reverse - forward,
            "phase_a_changes_forward",
            phase_changes_forward[0],
            "phase_b_changes_forward",
            phase_changes_forward[1],
            "phase_a_changes_reverse",
            phase_changes_reverse[0],
            "phase_b_changes_reverse",
            phase_changes_reverse[1],
        )

    print("MOTOR_ENCODER_TEST_DONE")
finally:
    for name, motor in motors:
        try:
            motor.SetPower(0)
            motor.Stop()
        except Exception as error:
            print("MOTOR_STOP_ERROR", name, error)
        try:
            motor.PWMPin.deinit()
        except Exception as error:
            print("PWM_CLEANUP_ERROR", name, error)

    for name, motor, encoder, encoder_id in encoders:
        try:
            encoder.deinit()
        except Exception as error:
            print("ENCODER_CLEANUP_ERROR", name, error)