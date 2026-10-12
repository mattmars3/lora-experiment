import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import board
import adafruit_ssd1306
import adafruit_rfm9x
import signal
import sys
import datetime
import argparse


args = get_args()
rfm9x = get_radio_handle(args)

total_expected = args.num_packets
total_received = 0

print("Listening for packets")
while True:
    try:
        # check for packet rx
        packet = rfm9x.receive(keep_listening=True, with_ack=False, timeout=None)

        if packet is None:
            pass
        else:
            # check the crc
            if rfm9x.crc_error():
                print("Packet failed CRC")
                continue

            # decode the packet
            packet_text = str(packet, "utf-8")
            parsed_seq = int(packet_text)
            seq_received = parsed_seq

            total_received += 1

            timestamp = datetime.datetime.now()
            readable_timestamp = timestamp.strftime("%H:%M:%S")
            print(f"{readable_timestamp}: {packet_text}")
    except KeyboardInterrupt:
        break

    except (UnicodeDecodeError, ValueError):
        print("Failed to receive packet with error!")
        continue


print(f"Received {total_received}/{total_expected} packets")
