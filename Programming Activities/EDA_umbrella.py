#Team member names: Annalise Dubeck, Daniel Mai, Emma Carothers
#Purpose of the code: Deploys an umbrella when a system detects darkness and moisture.
#Date code was started: 9/23/2026
#Date of last update: 9/23/2026
#Explanation of AI use: Coded the program and helped set up the circuit

from machine import Pin, ADC, PWM
import time

# -----------------------------
# PIN SETUP
# -----------------------------

# Button
BUTTON_PIN = 5          # D2 / GPIO5

# LED
LED_PIN = 6             # D3 / GPIO6

# Servo
SERVO_PIN = 18          # D9 / GPIO18

# Analog sensors
LIGHT_PIN = 1           # A0 / GPIO1
MOISTURE_PIN = 2        # A1 / GPIO2


# -----------------------------
# CREATE COMPONENT OBJECTS
# -----------------------------

button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

led = Pin(LED_PIN, Pin.OUT)
led.off()

light_sensor = ADC(Pin(LIGHT_PIN))
moisture_sensor = ADC(Pin(MOISTURE_PIN))


# -----------------------------
# SERVO SETUP
# -----------------------------

servo = PWM(Pin(SERVO_PIN), freq=50)


def servo_angle(angle):
    """
    Move SG90 to an angle from 0 to 180 degrees.
    """
    # Approximate SG90 pulse range:
    # 0 degrees   -> ~0.5 ms
    # 180 degrees -> ~2.5 ms

    min_us = 500
    max_us = 2500

    pulse_us = min_us + (max_us - min_us) * angle / 180

    # 50 Hz = 20,000 microsecond period
    duty = int(pulse_us * 65535 / 20000)

    servo.duty_u16(duty)


# -----------------------------
# UMBRELLA POSITIONS
# -----------------------------

UMBRELLA_DOWN = 0
UMBRELLA_UP = 90

servo_angle(UMBRELLA_DOWN)


# -----------------------------
# SENSOR THRESHOLDS
# -----------------------------

DARK_THRESHOLD = 30000
MOISTURE_THRESHOLD = 4000
REQUIRED_READINGS = 5

dark_count = 0
wet_count = 0


# -----------------------------
# SYSTEM STATE
# -----------------------------

system_on = False
umbrella_deployed = False


# -----------------------------
# BUTTON DEBOUNCING
# -----------------------------

last_button_state = 1


def check_button():
    global system_on

    # Wait for a button press
    if button.value() == 0:
        time.sleep_ms(50)  # debounce

        # Make sure it really is pressed
        if button.value() == 0:
            system_on = not system_on

            # Update LED immediately
            led.value(system_on)

            print("System ON" if system_on else "System OFF")

            # Wait for button release
            while button.value() == 0:
                time.sleep_ms(10)

            time.sleep_ms(50)  # debounce release


# -----------------------------
# SENSOR FUNCTIONS
# -----------------------------

def light_is_dark():
    value = light_sensor.read_u16()

    print("Light:", value)

    return value > DARK_THRESHOLD


def moisture_detected():
    value = moisture_sensor.read_u16()

    print("Moisture:", value)

    return value > MOISTURE_THRESHOLD


# -----------------------------
# UMBRELLA CONTROL
# -----------------------------

def deploy_umbrella():
    global umbrella_deployed

    if not umbrella_deployed:
        print("Deploying umbrella...")
        servo_angle(UMBRELLA_UP)
        umbrella_deployed = True


def retract_umbrella():
    global umbrella_deployed

    if umbrella_deployed:
        print("Retracting umbrella...")
        servo_angle(UMBRELLA_DOWN)
        umbrella_deployed = False


# -----------------------------
# MAIN LOOP
# -----------------------------

print("Automatic Umbrella System")
print("Starting...")

servo_angle(UMBRELLA_DOWN)
led.off()

while True:

    check_button()

    if system_on:

        light_value = light_sensor.read_u16()
        moisture_value = moisture_sensor.read_u16()

        dark = light_value > DARK_THRESHOLD
        wet = moisture_value > MOISTURE_THRESHOLD

        print("Light:", light_value)
        print("Moisture:", moisture_value)
        print("Dark:", dark)
        print("Wet:", wet)

        # Count consecutive dark readings
        if dark:
            dark_count += 1
        else:
            dark_count = 0

        # Count consecutive wet readings
        if wet:
            wet_count += 1
        else:
            wet_count = 0

        # Deploy only when BOTH conditions
        # have been true several times
        if dark_count >= REQUIRED_READINGS and wet_count >= REQUIRED_READINGS:
            deploy_umbrella()
        else:
            retract_umbrella()

    else:
        dark_count = 0
        wet_count = 0
        retract_umbrella()

    time.sleep_ms(200)