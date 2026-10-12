import time
import busio
import datetime
import sys

from test_args import get_args
from test_util import get_radio_handle
from logs import PacketInfo, ReceiverMeta, receive_and_parse_packet, write_recv_data, write_recv_metadata

args = get_args()
rfm9x = get_radio_handle(args)

total_successfully_received = 0
all_packets = []

transmission_start_ns = None
transmission_end_ns = None

print("Listening for packets")
while True:
    try:
        # check for packet rx
        packet_info = receive_and_parse_packet(rfm9x)
        if packet_info is not None:
            if not packet_info.crc_error:
                total_successfully_received += 1

                if transmission_start_ns == None:
                    transmission_start_ns = time.perf_counter_ns()

            transmission_end_ns = time.perf_counter_ns()
            all_packets.append(packet_info)

    except KeyboardInterrupt:
        break

    except (UnicodeDecodeError, ValueError):
        print("Failed to receive packet with error!")
        continue

if transmission_start_ns is None or transmission_end_ns is None:
    print("Failed to receive any packets")
    sys.exit(1)

# derived metadata values
total_payload_received = sum(map(lambda packet: packet.payload_size, all_packets))
transmission_duration = (transmission_end_ns - transmission_start_ns)

# show some diagnostics
elapsed_seconds = transmission_duration / 1_000_000_000
bytes_per_second = total_payload_received / elapsed_seconds

# now save and organize all of the information
timestamp = datetime.datetime.now()
file_timestamp = timestamp.strftime("%y%m%d-%I%M%S")

print(f"\n\t--- {total_payload_received} bytes transmitted over {elapsed_seconds:.3f} seconds at {bytes_per_second:.3f} bps")
print(f"\t--- {total_successfully_received}/{args.num_packets} received")
print(f"\t--- Data written with prefix {file_timestamp}")

write_recv_data(all_packets, file_timestamp)

# TODO: add support for distance guessing and other notes in metadata
meta = ReceiverMeta(args, total_payload_received, transmission_duration)
write_recv_metadata(meta, file_timestamp)
