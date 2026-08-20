import time
import board
import busio
from adafruit_pca9685 import PCA9685

# =========================
# I2C setup
# =========================

i2c = busio.I2C(board.SCL, board.SDA)

pca = PCA9685(i2c)

# PCA9685 PWM frequency
pca.frequency = 1000


# =========================
# Motor settings
# =========================

MOTOR_CHANNELS = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
]

# 30% vibration strength
MOTOR_POWER = int(0xFFFF * 0.30)

TEST_DURATION = 1.0
WAIT_DURATION = 0.5


# =========================
# Motor control
# =========================

def motor_on(channel, power=MOTOR_POWER):
    pca.channels[channel].duty_cycle = power


def motor_off(channel):
    pca.channels[channel].duty_cycle = 0


def all_motors_off():
    for channel in MOTOR_CHANNELS:
        motor_off(channel)


# =========================
# Test
# =========================

print("PCA9685 motor test started.")
print("Testing channels 0 to 7.")
print()

try:

    for channel in MOTOR_CHANNELS:

        print(f"Motor channel {channel}: ON")

        motor_on(channel)

        time.sleep(TEST_DURATION)

        motor_off(channel)

        print(f"Motor channel {channel}: OFF")

        time.sleep(WAIT_DURATION)

    print()
    print("Motor test complete.")

except KeyboardInterrupt:

    print()
    print("Test interrupted.")

finally:

    all_motors_off()

    pca.deinit()

    print("All motors OFF.")