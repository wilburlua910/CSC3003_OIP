import constants
import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib
# 156 steps for 3.2 cm?

# Lower level control
def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def setup_output_pin(pin: int):
    setup()
    GPIO.setup(pin, GPIO.OUT)

def setup_input_pin(pin: int):
    setup()
    GPIO.setup(pin, GPIO.IN)

def set_pin_high(pin: int):
    setup_output_pin(pin)
    GPIO.output(pin, GPIO.HIGH)

def set_pin_low(pin: int):
    setup_output_pin(pin)
    GPIO.output(pin, GPIO.LOW)

def get_pin_level(pin: int) -> int:
    setup_input_pin(pin)
    return GPIO.input(pin)

def move_stepper_motor(motor: list, distance_cm: float):
    pass
    #RpiMotorLib.BYJMotor().motor_run(motor, (distance_cm * constants.HALF_STEPS_TO_1CM))

# Higher level control
turn_on_ringlight = set_pin_high(constants.LEDPIN)

turn_off_ringlight = set_pin_low(constants.LEDPIN)

signal_start_cleaning = set_pin_high(constants.START_CLEANING_PIN)

signal_stop_cleaning = set_pin_high(constants.STOP_PIN)

def cleanup_signal_pins():
    set_pin_low(constants.START_CLEANING_PIN)
    set_pin_low(constants.STOP_PIN)

get_signal_done_cleaning = get_pin_level(constants.DONE_CLEANING_PIN)

move_count = 0

def goto_next_grid() -> bool:
    global move_count
    if move_count < constants.MAX_MOVES:
        move_stepper_motor(constants.MOTOR2, constants.GRID_SIDE_LENGTH)
        move_count = move_count + 1
        return True
    return False

def return_to_rest():
    global move_count
    move_count = 0
    pass

# TODO: how to make the stop signal and the listening bit?
