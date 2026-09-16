#Team member names: Annalise Dubeck, Daniel Mai, Emma Carothers
#Purpose of the code: Moves a servo 180 degrees when a button is pressed.
#Date code was started: 9/16/2026
#Date of last update: 9/16/2026
#Explanation of AI use: Helped set up circuit and coded the majority of the program

from machine import ADC, Pin
import time
import os

# -----------------------------
# Configuration
# -----------------------------

ADC_PIN = "A0"

ADC_MAX = 4095
ADC_VOLTAGE = 3.3

SAMPLE_INTERVAL = 1000  # 1 second between readings


# -----------------------------
# Find next available filename
# -----------------------------

run_number = 1

while True:
    filename = "rain_{:03d}.csv".format(run_number)

    try:
        os.stat(filename)
        run_number += 1
    except OSError:
        break


# -----------------------------
# Set up ADC
# -----------------------------

adc = ADC(Pin(ADC_PIN))
adc.atten(ADC.ATTN_11DB)


# -----------------------------
# Create new file
# -----------------------------

with open(filename, "w") as file:
    file.write("Voltage (V)\n")


print("Rain sensor started")
print("Writing 10 readings to:", filename)


# -----------------------------
# Take 10 readings
# -----------------------------

for i in range(10):

    # Read ADC
    adc_value = adc.read()

    # Convert ADC value to voltage
    voltage = (adc_value / ADC_MAX) * ADC_VOLTAGE

    # Print reading
    print("Reading {}: {:.3f} V".format(i + 1, voltage))

    # Write voltage to CSV
    with open(filename, "a") as file:
        file.write("{:.3f} V\n".format(voltage))

    # Wait before next reading
    time.sleep_ms(SAMPLE_INTERVAL)


print("Finished 10 readings.")
print("File saved:", filename)
