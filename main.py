"""A program for triggering outputs with a pulse if input is below a threshold time or keep it enabled until input is released."""

from machine import Pin, Timer
from micropython import const
from time import ticks_diff, ticks_ms, sleep_ms

# constants definitions
PULSE_THRESHOLD_MS = const(1000)  # time below output is triggered with a pulse
PULSE_TIME_DEFAULT = const(500)  # default pulse time

# input pins definitions
button_1 = Pin(18, Pin.IN, Pin.PULL_UP)
button_2 = Pin(20, Pin.IN, Pin.PULL_UP)
button_3 = Pin(21, Pin.IN, Pin.PULL_UP)
button_4 = Pin(22, Pin.IN, Pin.PULL_UP)
input_1 = Pin(3, Pin.IN, Pin.PULL_UP)
input_2 = Pin(4, Pin.IN, Pin.PULL_UP)
input_3 = Pin(5, Pin.IN, Pin.PULL_UP)
input_4 = Pin(6, Pin.IN, Pin.PULL_UP)
input_5 = Pin(7, Pin.IN, Pin.PULL_UP)
input_6 = Pin(8, Pin.IN, Pin.PULL_UP)
input_7 = Pin(14, Pin.IN, Pin.PULL_UP)
input_8 = Pin(15, Pin.IN, Pin.PULL_UP)

# output pins definitions
output_1 = Pin(13, Pin.OUT)
output_2 = Pin(12, Pin.OUT)
output_3 = Pin(28, Pin.OUT)
output_4 = Pin(27, Pin.OUT)
output_5 = Pin(26, Pin.OUT)
output_6 = Pin(19, Pin.OUT)
output_7 = Pin(17, Pin.OUT)
output_8 = Pin(16, Pin.OUT)

INPUT_TRIGGER_TICK_MAP = {}


def check_input(input_pin: Pin, output_pin: Pin, pulse_time=PULSE_TIME_DEFAULT) -> None:
    """Check input pin status and enable the output."""
    is_input_triggered = input_pin.value() == 0
    # button pressed track press tick
    if INPUT_TRIGGER_TICK_MAP.get(input_pin) is None and is_input_triggered:
        INPUT_TRIGGER_TICK_MAP[input_pin] = ticks_ms()
    if input_pin in INPUT_TRIGGER_TICK_MAP:
        time_diff = abs(ticks_diff(INPUT_TRIGGER_TICK_MAP[input_pin], ticks_ms()))
        # pulse, enable the output and spawn a timer for disabling it after pulse_time
        if time_diff < PULSE_THRESHOLD_MS and not is_input_triggered:
            output_pin.on()
            Timer(
                period=pulse_time,
                mode=Timer.ONE_SHOT,
                callback=lambda t: output_pin.off(),
            )
            del INPUT_TRIGGER_TICK_MAP[input_pin]
        # long press keep output on after the threshold
        elif time_diff > PULSE_THRESHOLD_MS and is_input_triggered:
            output_pin.on()
        # input released output off and cleanup tick map
        elif not is_input_triggered:
            output_pin.off()
            del INPUT_TRIGGER_TICK_MAP[input_pin]


if __name__ == "__main__":
    while True:
        check_input(input_1, output_1)
        check_input(input_2, output_2, 250)
        check_input(input_3, output_3)
        check_input(input_4, output_4)
        check_input(input_5, output_5)
        check_input(input_6, output_6)
        check_input(input_7, output_7)
        check_input(input_8, output_8)
        check_input(button_1, output_1)
        check_input(button_2, output_2, 250)
        check_input(button_3, output_3)
        check_input(button_4, output_4)
        sleep_ms(10)
