import time
import busio
import datetime

from test_args import get_args, write_recv_metadata
from test_util import get_radio_handle
from logs import PacketInfo, receive_and_parse_packet, write_recv_data

args = get_args()
rfm9x = get_radio_handle(args)

total_successfully_received = 0
all_packets = []

# TODO: Add support for a control-plane that can be used to semi-accurately
#       signal a stop and start to be used in bandwidth measurements

print("Listening for packets")
while True:
    try:
        # check for packet rx
        packet_info = receive_and_parse_packet(rfm9x)
        if packet_info is not None:
            if not packet_info.crc_error:
                total_successfully_received += 1
            all_packets.append(packet_info)

    except KeyboardInterrupt:
        break

    except (UnicodeDecodeError, ValueError):
        print("Failed to receive packet with error!")
        continue


timestamp = datetime.datetime.now()
file_timestamp = timestamp.strftime("%y%m%d-%I%M%S")

print(f"\t--- {total_successfully_received}/{args.num_packets} received ---")
print(f"\t--- Data written with prefix {file_timestamp} ---")

write_recv_data(all_packets, file_timestamp)
# TODO: add support for distance guessing and other notes in metadata
write_recv_metadata(args, file_timestamp)
