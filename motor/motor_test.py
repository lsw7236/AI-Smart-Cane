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
# 8-direction motor mapping
# =========================

MOTOR_MAP = {
    "FRONT": 0,
    "FRONT_RIGHT": 1,
    "RIGHT": 2,
    "BACK_RIGHT": 3,
    "BACK": 4,
    "BACK_LEFT": 5,
    "LEFT": 6,
    "FRONT_LEFT": 7,
}


# =========================
# Motor settings
# =========================

DEFAULT_POWER = 0.30
TEST_DURATION = 1.0
WAIT_DURATION = 0.5


# =========================
# Motor control
# =========================

def power_to_duty(power):
    power = max(0.0, min(power, 1.0))
    return int(0xFFFF * power)


def motor_on(channel, power=DEFAULT_POWER):
    pca.channels[channel].duty_cycle = power_to_duty(power)


def motor_off(channel):
    pca.channels[channel].duty_cycle = 0


def all_motors_off():
    for channel in MOTOR_MAP.values():
        motor_off(channel)


# =========================
# Direction test
# =========================

def test_direction(name, channel):
    print(
        f"{name} "
        f"(CH{channel}) -> ON"
    )

    motor_on(channel)

    time.sleep(TEST_DURATION)

    motor_off(channel)

    print(
        f"{name} "
        f"(CH{channel}) -> OFF"
    )

    time.sleep(WAIT_DURATION)


# =========================
# Main
# =========================

print("8-direction motor test started.")
print()

try:

    for direction, channel in MOTOR_MAP.items():
        test_direction(
            direction,
            channel
        )

    print()
    print("All direction tests complete.")

except KeyboardInterrupt:

    print()
    print("Test interrupted.")

finally:

    all_motors_off()

    pca.deinit()

    print("All motors OFF.")