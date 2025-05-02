import os

path = os.path.abspath(__file__)
path = path.replace(f"globals.py", "")


PROJPATH = path

IMG_X = 240
IMG_Y = 320

NUM_SMPLS = 10

OUTPUT_PATH = f"{PROJPATH}data/output.txt"

INFOMSG = f"""
Resolution:                 {IMG_X} x {IMG_Y}
Crop images:                maybeeee
Default number of samples:  10
Output path:                {OUTPUT_PATH}
"""

HELPMSG = """
    NORMAL USE:
info:           Display basic information about the system
open:           Try to open a new serial connection to the scanner
close:          If the connection is open, close it
lon:            Light up the laser
loff:           Turn off the laser
mov [angle]:    Move the motor to a desired angle
clear           Delete photos taken during the scanning process
prev            Take a single photo and display it
scan [mode]     Perform a complete 360° scan
                Modes:
                    (blank):    normal scan
                    pic:        only take pictures, do not move the motor
                    mov:        only move the motor, do not take pictures
quit:           Exit the program

    ADVANCED:
path:           Display the directory of this program
msg [message]   Send an internal instruction directly to the scanner
echo [message]  Just like "msg" but wait for a rensponse from the scanner
crop [y / n]    Set if we want to crop the images in half
ovrd [pin] [0 / 1] Override a pin on the Arduino board to 0 or 1
"""

if __name__ == "__main__":
    print(path)