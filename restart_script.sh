#!/bin/bash

while true; do
    echo "Starting the bot..."
    python Bot/__main__.py
    echo "Restarting in 6 hours..."
    sleep 21600 # 6 hours in seconds
done
