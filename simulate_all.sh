#!/bin/bash

# Run all board simulations for 1,000, 10,000, 100,000, and 1,000,000 games using Strategy 1
python3 board.py 1 1000
python3 board.py 1 10000
python3 board.py 1 100000
python3 board.py 1 1000000

# Run all board simulations for 1,000, 10,000, 100,000, and 1,000,000 games using Strategy 2
python3 board.py 2 1000
python3 board.py 2 10000
python3 board.py 2 100000
python3 board.py 2 1000000