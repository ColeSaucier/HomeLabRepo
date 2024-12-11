#!/bin/bash

echo "Press 9 to log time to MS"

# Function to log the time when a key is pressed
log_time() {
    echo -e "\nKey pressed at $(date '+%H:%M:%S.%3N')"
}

# Main loop to wait for key press
while true; do
    read -n 1 key
    case $key in
        9)
            log_time 9
            ;;
        q)
            echo -e "\nExiting..."
            exit 0
            ;;
    esac
done
