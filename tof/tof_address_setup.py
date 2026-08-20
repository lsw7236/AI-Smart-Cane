import time
import board
import busio
import digitalio
import adafruit_vl53l1x

# I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# XSHUT GPIO pins for 8 ToF sensors
XSHUT_PINS = [
    board.D5,
    board.D6,
    board.D13,
    board.D16,
    board.D19,
    board.D20,
    board.D21,
    board.D26,
]

# I2C addresses for 8 ToF sensors
NEW_ADDRESSES = [
    0x2A,  # BOTTOM_LEFT
    0x2B,  # BOTTOM_LEFT_CENTER
    0x2C,  # BOTTOM_CENTER
    0x2D,  # BOTTOM_RIGHT_CENTER
    0x2E,  # BOTTOM_RIGHT
    0x2F,  # TOP_LEFT
    0x30,  # TOP_CENTER
    0x31,  # TOP_RIGHT
]

# XSHUT control objects
xshut = []

print("Initializing XSHUT pins...")

# Disable all ToF sensors
for pin in XSHUT_PINS:
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.OUTPUT
    io.value = False
    xshut.append(io)

time.sleep(0.5)

print("Starting ToF address setup...")

sensors = []

for i in range(len(XSHUT_PINS)):

    # Enable one sensor
    xshut[i].value = True

    time.sleep(0.2)

    # Sensor starts at default address 0x29
    sensor = adafruit_vl53l1x.VL53L1X(
        i2c,
        address=0x29
    )

    # Change I2C address
    sensor.set_address(
        NEW_ADDRESSES[i]
    )

    sensors.append(sensor)

    print(
        f"ToF {i + 1}: "
        f"0x29 -> 0x{NEW_ADDRESSES[i]:02X}"
    )

print()
print("All ToF addresses configured.")