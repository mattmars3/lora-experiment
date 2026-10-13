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

def craft_payload(seq: int, size: int) -> bytes:
    padded = str(seq).zfill(size)
    if size < 0 or size > 252: # 252 is limit for library
        raise ValueError("Seq is too large for specified size")
    return padded.encode("utf-8")

# initialize run parameters
seq = 0
total_payload_bytes_transmitted = 0

# TODO: ensure that this cannot fail and we won't need csv logging
# easier to ensure a good test than fix timeouts

for i in range(args.num_packets):
    # Craft the message to send, and send it
    payload_size = 25

    payload = craft_payload(seq, 25)
    succeeded = rfm9x.send(payload)

    if not succeeded:
        # failed because of timeout
        print(f"Failed to send packet {seq}")
    else:
        # log a successful send
        total_payload_bytes_transmitted += payload_size
        print(f"Sent seq #{seq}")

    seq += 1

print(f"\n\t ---{total_payload_bytes_transmitted} total bytes transmitted")
