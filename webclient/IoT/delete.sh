#!/bin/bash
#
# Script that pushes the scripts folders to the pycom board
#

# Default variables
PORT=/dev/ttyACM0
DEST_DIR=/flash/*

# Makes it possible to override parameters with -p -s -d
while getopts p:s:d: option
do
    case "${option}"
        in
            p) PORT=${OPTARG};;
            d) DEST_DIR${OPTARG};;
    esac
done

function delete() {
    python -m there -p $PORT rm -r "$DEST_DIR"
}

echo "Deleting to device: " $PORT
echo "  Files:" $SRC_DIR "to" $DEST_DIR

delete

echo "Listing uploaded files on device: " $PORT
echo "  " $(python -m there --reset -p $PORT ls /flash)