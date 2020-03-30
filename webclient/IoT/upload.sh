#!/bin/bash
#
# Script that pushes the scripts folders to the pycom board
#

# Default variables
PORT=/dev/ttyACM0
SRC_DIR=scripts/*
DEST_DIR=/flash/

# Makes it possible to override parameters with -p -s -d
while getopts p:s:d: option
do
    case "${option}"
        in
            p) PORT=${OPTARG};;
            s) SRC_DIR=${OPTARG};;
            d) DEST_DIR${OPTARG};;
    esac
done

#
# Parameter $1: The port to upload to e.g. /dev/ttyACM0 or /dev/ttyACM1 ..
function upload() {
    python -m there -p $PORT push --recursive --force $SRC_DIR $DEST_DIR
}

echo "Uploading to device: " $PORT
echo "  Files:" $SRC_DIR "to" $DEST_DIR

upload

echo "Listing uploaded files on device: " $PORT
# reset: do a soft reset on the end
CMD=$(python -m there --reset -p $PORT ls $DEST_DIR)
echo $CMD