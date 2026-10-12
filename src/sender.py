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

from test_args import get_args
from test_util import get_radio_handle

args = get_args()
rfm9x = get_radio_handle(args)

# initialize run parameters
seq = 0
logs = []

for i in range(args.num_packets):
    # Craft the message to send, and send it
    payload = bytes(f"{seq}","utf-8")
    succeeded = rfm9x.send(payload)

    if not succeeded:
        # failed because of timeout
        print(f"Failed to send packet {seq}")
    else:
        # log a successful send
        print(f"Sent seq #{seq}")

    seq += 1
    time.sleep(0.02)
