# Matt Marsico 10/11/2026
# LoRa Testing Framework
# GPL License

import sys
import time
import math

from test_args import get_args
from test_util import get_radio_handle

args = get_args()
rfm9x = get_radio_handle(args)

# initialize run parameters
seq = 0
logs = []

# TODO: ensure that this cannot fail and we won't need csv logging
# easier to ensure a good test than fix timeouts

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
