import time
import board
import busio
import adafruit_vl53l1x

# =========================
# I2C setup
# =========================

i2c = busio.I2C(board.SCL, board.SDA)


# =========================
# ToF sensor configuration
# =========================

SENSOR_CONFIG = [
    {
        "name": "BOTTOM_LEFT",
        "address": 0x2A,
    },
    {
        "name": "BOTTOM_LEFT_CENTER",
        "address": 0x2B,
    },
    {
        "name": "BOTTOM_CENTER",
        "address": 0x2C,
    },
    {
        "name": "BOTTOM_RIGHT_CENTER",
        "address": 0x2D,
    },
    {
        "name": "BOTTOM_RIGHT",
        "address": 0x2E,
    },
    {
        "name": "TOP_LEFT",
        "address": 0x2F,
    },
    {
        "name": "TOP_CENTER",
        "address": 0x30,
    },
    {
        "name": "TOP_RIGHT",
        "address": 0x31,
    },
]


# =========================
# Connect sensors
# =========================

print("Connecting to ToF sensors...")
print()

sensors = []

for config in SENSOR_CONFIG:

    sensor = adafruit_vl53l1x.VL53L1X(
        i2c,
        address=config["address"]
    )

    # Long range mode
    sensor.distance_mode = 2

    # Measurement timing budget
    sensor.timing_budget = 100

    sensor.start_ranging()

    sensors.append(
        {
            "name": config["name"],
            "address": config["address"],
            "sensor": sensor,
        }
    )

    print(
        f'{config["name"]} connected '
        f'(0x{config["address"]:02X})'
    )


print()
print("All ToF sensors connected.")
print("Press Ctrl+C to stop.")
print()


# =========================
# Read sensors
# =========================

try:

    while True:

        output = []

        for item in sensors:

            sensor = item["sensor"]
            name = item["name"]

            if sensor.data_ready:

                distance = sensor.distance

                sensor.clear_interrupt()

                if distance is not None:

                    output.append(
                        f"{name}: {distance:.1f} cm"
                    )

                else:

                    output.append(
                        f"{name}: ---"
                    )

            else:

                output.append(
                    f"{name}: ---"
                )

        print(" | ".join(output))

        time.sleep(0.1)


# =========================
# Stop sensors
# =========================

except KeyboardInterrupt:

    print()
    print("Stopping ToF sensors...")

    for item in sensors:

        item["sensor"].stop_ranging()

    print("Program terminated.")