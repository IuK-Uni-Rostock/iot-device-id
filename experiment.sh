#!/bin/bash
set -x

export LOG_FILE="experiment-log $(date).txt"
echo $@ >> "${LOG_FILE}"

timeout=90  # seconds

read -p "Please restart device and press enter to continue"
timeout --foreground -k 125 120 python3 ./cli.py record $@

read -p "Please restart device and press enter to continue"
echo "--- next run ---" >> "${LOG_FILE}"
timeout --foreground -k 125 120 python3 ./cli.py detect

read -p "Please restart device and press enter to continue"
echo "--- next run ---" >> "${LOG_FILE}"
timeout --foreground -k 125 120 python3 ./cli.py detect

read -p "Please restart device and press enter to continue"
echo "--- next run ---" >> "${LOG_FILE}"
timeout --foreground -k 125 120 python3 ./cli.py detect

echo "Experiment finished successfully" >> "${LOG_FILE}"
