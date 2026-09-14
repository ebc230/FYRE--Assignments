from machine import Pin, ADC
import time


# ==========================================
# PIN SETUP
# ==========================================

button = Pin("D2", Pin.IN, Pin.PULL_UP)

green_led = Pin("D8", Pin.OUT)

blue_led = Pin("D9", Pin.OUT)

light_sensor = ADC(Pin("A0"))


# ==========================================
# SETTINGS
# ==========================================

LIGHT_THRESHOLD = 30000

FLASH_TIME = 250


# ==========================================
# INITIAL STATE
# ==========================================

# The button determines this.
# False = alarm OFF
# True  = alarm ON

alarm_on = False

green_led.off()
blue_led.off()

last_button_state = 1


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    # --------------------------------------
    # BUTTON
    # --------------------------------------

    button_state = button.value()

    # Detect a button press
    if button_state == 0 and last_button_state == 1:

        # Change alarm state
        alarm_on = not alarm_on

        if alarm_on:

            # ==============================
            # ALARM ON
            # ==============================

            green_led.on()

            # Blue starts OFF
            blue_led.off()

            print("ALARM ARMED")

        else:

            # ==============================
            # ALARM OFF
            # ==============================

            green_led.off()

            # IMPORTANT:
            # Blue MUST turn off whenever
            # the alarm is turned off.
            blue_led.off()

            print("ALARM DISARMED")

        # Button debounce
        time.sleep_ms(200)

    last_button_state = button_state


    # --------------------------------------
    # ONLY CHECK SENSOR IF ALARM IS ON
    # --------------------------------------

    if alarm_on:

        light_value = light_sensor.read_u16()

        print("Light:", light_value)

        # Photoresistor is ONLY allowed to
        # control blue LED when alarm_on=True
        if light_value > LIGHT_THRESHOLD:

            blue_led.on()
            time.sleep_ms(FLASH_TIME)

            blue_led.off()
            time.sleep_ms(FLASH_TIME)

        else:

            blue_led.off()

    else:

        # ==================================
        # ALARM OFF
        # ==================================
        #
        # This guarantees that the blue LED
        # can NEVER be on while the green LED
        # / alarm is off.

        blue_led.off()


    time.sleep_ms(10)
