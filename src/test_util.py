def get_radio_handle(args, display=True):
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
    rfm9x.signal_bandwidth = args.bandwidth * 1000
    rfm9x.preamble_length = args.preamble_length

    if display:
        print("---------------------------------------------------------")
        print("Running LoRa with the following parameters:")
        print(f"\tcoding rate: {args.coding_rate}")
        print(f"\tspreading factor: {args.spreading_factor}")
        print(f"\tbandwidth: {args.bandwidth} kHz")
        print(f"\tpreamble length: {args.preamble_length}")
        print(f"\tnum packets: {args.num_packets}")
        print("---------------------------------------------------------")

    return rfm9x
