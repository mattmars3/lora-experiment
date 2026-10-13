import time
import busio
import datetime
import pickle

class SenderRecord:
    def __init__(self, seq, timestamp):
        self.seq = seq
        self.timestamp = timestamp

    def to_csv_row(self):
        return f"{seq},{timestamp}"

# +++ RECEIVER DATA BELOW

# represents either an intact received packet, or one that failed CRC
class PacketInfo:
    def __init__(self, timestamp, crc_error, seq, last_rssi, last_snr, payload_size):
        self.timestamp = timestamp
        self.crc_error = crc_error
        self.seq = seq # can be None
        self.last_rssi = last_rssi # can be None
        self.last_snr = last_snr # can be None
        self.payload_size = payload_size

    def to_csv_row(self) -> str:
        return f"{self.timestamp},{self.crc_error},{self.seq},{self.last_rssi},{self.last_snr},{self.payload_size}"

def receive_and_parse_packet(rfm9x) -> PacketInfo | None:
    packet: bytearray | None = rfm9x.receive(keep_listening=True, with_ack=False, timeout=None)

    if packet is None:
        return None
    else:
        # check the crc
        crc_error = rfm9x.crc_error()
        timestamp = time.time()

        if not crc_error:
            # decode the packet
            packet_text = str(packet, "utf-8")
            parsed_seq = int(packet_text)

            payload_size = len(packet)
            
            packet_info = PacketInfo(timestamp, crc_error, parsed_seq,
                                rfm9x.last_rssi, rfm9x.last_snr, payload_size)

            return packet_info
        else:
            packet_info = PacketInfo(timestamp, crc_error, None, None, None, None)
            print("Packet failed CRC")
            return packet_info


def write_recv_data(all_packets, file_timestamp):
    filename = f"data/{file_timestamp}-recv.csv"
    # output the actual results
    with open(filename, 'w') as output:
        for packet in all_packets:
            output.write(packet.to_csv_row() + "\n")

# +++ RECEIVER METADATA BELOW

class ReceiverMeta:
    def __init__(self, args, total_payload_received, transmission_duration):
        self.args = args
        self.total_payload_received = total_payload_received
        self.transmission_duration = transmission_duration

    def write_recv_metadata(self, file_timestamp: str):
        filename = f"data/{file_timestamp}-recv-meta.pkl"
        with open(filename, "ab") as output:
            pickle.dump(self, output)

    @classmethod
    def read_recv_metadata(cls, file_timestamp: str):
        filename = f"data/{file_timestamp}-recv-meta.pkl"
        with open(filename, "rb") as file:
            return pickle.load(file)
