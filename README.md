# LoRa Experiment
Project to examine the different tunable parameters of LoRa and measure their affects
on network properties.

## Equipment
This project was conducted using two Raspberry Pi 4s with an Adafruit RFM95W LoRa Bonnet.

## Installation and Setup
Start by cloning the directory on two Raspberry Pis
```sh
cd
git clone https://github.com/mattmars3/lora-experiment
```

Next, you need to install all necessary dependencies; this guide assumes Raspberry Pi OS.
```sh
sudo apt update && sudo apt install python3 uv python3-dev i2c-tools
```

Then, enter the project directory and install the python library dependencies.
```sh

```

Finally, ssh into one of the pis and start the receiver. Then, in a different window, start the sender.
```sh
# on the receiver pi
cd lora-experiment
uv run src/receiver.py \
  --coding-rate 5 \
  --spreading-factor 7 \
  --bandwidth 250 \
  --preamble-length 8 \
  --num-packets 500

# then, on the receiver
cd lora-experiment
uv run src/sender.py \
  --coding-rate 5 \
  --spreading-factor 7 \
  --bandwidth 250 \
  --preamble-length 8 \
  --num-packets 500
```

Finally, after the sender is done transmitting, press CTRL-C on the receiver which will 
shut it down and save the test run data to a file.

## Applications
Consider adding an interesting end-to-end application that utilizes LoRa and explain why
it uses the parameters that it does. Stream an image, text block, midi song, etc.
