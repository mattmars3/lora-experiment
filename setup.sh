#!/bin/sh

sudo apt update && sudo apt install --yes git python3 uv python3-dev i2c-tools neovim

uv venv
source .venv/bin/activate

uv pip install adafruit-circuitpython-ssd1306
uv pip install adafruit-circuitpython-framebuf
uv pip install adafruit-circuitpython-rfm9x
uv pip install RPi.GPIO
