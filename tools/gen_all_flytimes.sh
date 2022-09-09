#!/usr/bin/env bash

set -e

echo "Generating DDR Channel A flytimes..."
python3 gen_flytimes.py ../qsbc.kicad_pcb DDR_flytimes.xlsx /DDR/ DDR_A

echo "Generating DDR Channel B flytimes..."
python3 gen_flytimes.py ../qsbc.kicad_pcb DDR_flytimes.xlsx /DDR/ DDR_B

