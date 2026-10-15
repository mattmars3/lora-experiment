import argparse

def get_args():
    parser = argparse.ArgumentParser(
        prog="LoRa Sender",
        description="LoRa testing program exposing tunable parameters",
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
    parser.add_argument(
        "-l", "--payload-size",
        help="Payload size to send per packet: 1 - 252 bytes",
        default=25
    )

    args = parser.parse_args()
    return args
