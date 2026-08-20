import time
import board
import busio
from adafruit_pca9685 import PCA9685


# =========================
# I2C / PCA9685 setup
# =========================

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)
pca.frequency = 1000


# =========================
# Motor channel mapping
# =========================
#
# Front direction motors used for YOLO object guidance.
#
# Final physical channel mapping can be changed later.
#

FRONT_LEFT = 0
FRONT_CENTER = 1
FRONT_RIGHT = 2


# =========================
# Motor settings
# =========================

DEFAULT_POWER = 0.30

MIN_POWER = 0.0
MAX_POWER = 1.0


# =========================
# Basic motor control
# =========================

def power_to_duty(power):
    power = max(MIN_POWER, min(power, MAX_POWER))

    return int(0xFFFF * power)


def motor_on(channel, power=DEFAULT_POWER):
    pca.channels[channel].duty_cycle = power_to_duty(power)


def motor_off(channel):
    pca.channels[channel].duty_cycle = 0


def all_front_motors_off():
    motor_off(FRONT_LEFT)
    motor_off(FRONT_CENTER)
    motor_off(FRONT_RIGHT)


# =========================
# Direction control
# =========================

def vibrate_left(power=DEFAULT_POWER):
    all_front_motors_off()

    motor_on(FRONT_LEFT, power)

    print("Direction: LEFT")


def vibrate_center(power=DEFAULT_POWER):
    all_front_motors_off()

    motor_on(FRONT_CENTER, power)

    print("Direction: CENTER")


def vibrate_right(power=DEFAULT_POWER):
    all_front_motors_off()

    motor_on(FRONT_RIGHT, power)

    print("Direction: RIGHT")


def stop_direction():
    all_front_motors_off()

    print("Direction: STOP")


# =========================
# X-coordinate direction
# =========================

def get_direction(x_center, frame_width):
    """
    Convert an object's X center coordinate
    into LEFT / CENTER / RIGHT.
    """

    left_boundary = frame_width / 3
    right_boundary = (frame_width / 3) * 2

    if x_center < left_boundary:
        return "LEFT"

    elif x_center < right_boundary:
        return "CENTER"

    else:
        return "RIGHT"


def guide_object(x_center, frame_width, power=DEFAULT_POWER):
    """
    Vibrate the motor corresponding to
    the detected object's position.
    """

    direction = get_direction(
        x_center,
        frame_width
    )

    if direction == "LEFT":
        vibrate_left(power)

    elif direction == "CENTER":
        vibrate_center(power)

    elif direction == "RIGHT":
        vibrate_right(power)

    return direction


# =========================
# Standalone test
# =========================

if __name__ == "__main__":

    print("Direction motor test started.")
    print()

    try:

        print("LEFT")
        vibrate_left()
        time.sleep(1)

        stop_direction()
        time.sleep(0.5)

        print("CENTER")
        vibrate_center()
        time.sleep(1)

        stop_direction()
        time.sleep(0.5)

        print("RIGHT")
        vibrate_right()
        time.sleep(1)

        stop_direction()

        print()
        print("Direction motor test complete.")

    except KeyboardInterrupt:

        print()
        print("Test interrupted.")

    finally:

        all_front_motors_off()
        pca.deinit()

        print("All motors OFF.")