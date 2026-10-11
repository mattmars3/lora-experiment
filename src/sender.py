# Matt Marsico 10/11/2026
# LoRa Testing Framework
# GPL License

import sys
import argparse
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
import signal
import sys
import math

parser = argparse.ArgumentParser(
    prog="LoRa Sender",
    description="LoRa sender program exposing tunable parameters",
)

parser.add_argument(
    "-c", "--coding-rate",
    help="Coding rate of the transmission: [5, 6, 7, 8]",
    choices=[5, 6, 7, 8],
    required=True, type=int
)
parser.add_argument(
    "-s", "--spreading-factor",
    help="LoRa spreading factor: [6, 7, 8, 9, 10, 11, 12]",
    choices=[6, 7, 8, 9, 10, 11, 12],
    required=True, type=int
)
parser.add_argument(
    "-b", "--bandwidth",
    help="Bandwidth option (kHz): [7.8, 10.4, 15.6, 20.8, 31.25, 41.7, 62.5, 125, 250]",
    choices=[7.8, 10.4, 15.6, 20.8, 31.25, 41.7, 62.5, 125.0, 250.0],
    required=True, type=float
)
parser.add_argument(
    "-p", "--preamble-length",
    help="Preamble length: 8 or greater",
    required=True, type=int
)
parser.add_argument(
    "-n", "--num-packets",
    help="Number of total packets to send to the receiver",
    required=True, type=int
)

args = parser.parse_args()
bandwidth = int(args.bandwidth * 1000)

print("---------------------------------------------------------")
print("Running LoRa sender with the following parameters:")
print(f"\tcoding rate: {args.coding_rate}")
print(f"\tspreading factor: {args.spreading_factor}")
print(f"\tbandwidth: {bandwidth} Hz")
print(f"\tpreamble length: {args.preamble_length}")
print(f"\tnum packets: {args.num_packets}")
print("---------------------------------------------------------")

# Create the I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# 128x32 OLED Display
reset_pin = DigitalInOut(board.D4)
display = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c, reset=reset_pin)
# Clear the display.
display.fill(0)
display.show()
width = display.width
height = display.height

# Configure LoRa Radio
CS = DigitalInOut(board.CE1)
RESET = DigitalInOut(board.D25)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, 915.0, crc = True)

# check bandwidth
if bandwidth not in rfm9x.bw_bins:
    print("Invalid bandwidth entered. Choose one of the following:\n",rfm9x.bw_bins)
    sys.exit(0)

# set tunable parameters
rfm9x.tx_power = 23
rfm9x.coding_rate = args.coding_rate
rfm9x.spreading_factor = args.spreading_factor
rfm9x.signal_bandwidth = args.bandwidth
rfm9x.preamble_length = args.preamble_length

# initialize run parameters
seq = 0
params_hash = hash("")
logs = []

for i in range(args.num_packets):
    # display progress on screen
    display.fill(0)
    percent_done = round(i * 100 / args.num_packets)
    if percent_done % 5 == 0:
        percent_text = f"Sending Packets: {percent_done}%"
        display.text(percent_text, 0, 0, 1, size=1)
        display.show()

    # Craft the message to send, and send it
    # button_c_data = bytes("Button C!\r\n","utf-8")
    # rfm9x.send(button_c_data, xmit_timeout=10)

    time.sleep(0.02)

display.fill(0)
display.text("DONE", 0, 0, 1, size=2)
display.text(f"Sent {args.num_packets} packets", 0, 18, 1, size=1)
display.show()
time.sleep(5)
display.fill(0)
display.show()
