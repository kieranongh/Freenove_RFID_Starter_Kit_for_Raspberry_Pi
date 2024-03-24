import time
import RPi.GPIO as GPIO  # Import the GPIO library for Raspberry Pi

SHORT_PULSE_DURATION = 316/1000000
LONG_PULSE_DURATION = 818/1000000
ATTEMPTS = 4
ADDRESS = 0x12340

RADIO_COMMANDS = {
    'ALL_ON': 0b00000100,
    'ALL_OFF': 0b00001000,
    'SWITCH_1_ON': 0b00001111,
    'SWITCH_1_OFF': 0b00001110,
    'SWITCH_2_ON': 0b00001101,
    'SWITCH_2_OFF': 0b00001100,
    'SWITCH_3_ON': 0b00001011,
    'SWITCH_3_OFF': 0b00001010,
    'SWITCH_4_ON': 0b00000111,
    'SWITCH_4_OFF': 0b00000110
}

def setup_gpio(pin):
    """Set up GPIO pin for output."""
    GPIO.setmode(GPIO.BOARD)  # Use board pin numbering
    GPIO.setup(pin, GPIO.OUT)  # Set pin as output

def reverse_bits(byte):
    """Reverse the bits of a byte."""
    return int('{:08b}'.format(byte)[::-1], 2)

def send_radio_packet(pin, data):
    """Send a packet via radio."""
    for _ in range(ATTEMPTS):
        for bit in reversed(range(32)):
            send_pulse(pin, (data >> bit) & 1)
        time.sleep(0.01)

def send_pulse(pin, is_long):
    """Send a pulse."""
    gpio_output(pin, 1)
    time.sleep(LONG_PULSE_DURATION if is_long else SHORT_PULSE_DURATION)
    gpio_output(pin, 0)
    time.sleep(SHORT_PULSE_DURATION if is_long else LONG_PULSE_DURATION)

def calculate_crc(data):
    """Calculate the CRC byte for data."""
    a = reverse_bits(data >> 16)
    b = reverse_bits(data >> 8)
    c = reverse_bits(data & 0xFF)
    return reverse_bits(a + b + c)

def make_packet(address, command):
    """Create a radio packet."""
    data = ((address & 0xFFFFF) << 4) | (command & 0xF)
    crc = calculate_crc(data)
    return (data << 8) | crc

def radio_switch(pin, switch_id, state):
    """Switch the radio."""
    if switch_id == "ALL":
        command = RADIO_COMMANDS["ALL_ON"] if state else RADIO_COMMANDS["ALL_OFF"]
    else:
        command = RADIO_COMMANDS[f'SWITCH_{switch_id}_{("ON" if state else "OFF")}']
    packet = make_packet(ADDRESS, command)
    send_radio_packet(pin, packet)
    time.sleep(2)

def gpio_output(pin, value):
    """Set GPIO pin output."""
    GPIO.output(pin, value)    # Set output value (1 for high, 0 for low)

# Example usage:
if __name__ == "__main__":
    PIN_NUMBER = 18  # Example GPIO pin number
    SWITCH_ID = 1
    STATE = False
    setup_gpio(PIN_NUMBER)
    radio_switch(PIN_NUMBER, SWITCH_ID, STATE)
