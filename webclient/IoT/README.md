# Template project for PyCom
Use this repo as a template for future projects for the PyCom. It contains the minimum necessary libraries to get started.

# Structure of the repo
* scripts/boot.py - first file to execute
* scripts/main.py - file that is executed after boot.py
* scripts/cert - certificates (if any)
* scripts/lib - all the libraries needed to run your project goes into this folder
* scripts/sys - sys folder


# Usage of upload/delete scripts
```bash
./upload.sh # Uploads (and overrides) all the contents located in the ./scripts folder
./upload.sh -s scripts/main.py # Uploads only the main.py file (usually this is handy when you want to upload only your main program)
./upload.sh -p /dev/ttyACM0 # Use the specified serial port
./upload.sh -d /flash/myDir # Upload to specified folder
```

```bash
./delete.sh # Deletes all contents located in /flash/
./delete.sh -p /dev/ttyACM0 # Use the specified serial port
./delete.sh -d /flash/myDir # Delete specified folder
```
