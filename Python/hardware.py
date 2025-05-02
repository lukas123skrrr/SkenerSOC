import serialCom as com
import time

motorSteps = 200

def setPosition(ser, angle):
    steps = int((motorSteps / 360) * angle)
    com.sendMessage(ser, f"mtr{steps}")
    com.waitForMessage(ser, "done")
    print(f"Moved the motor to {steps} steps")

def pinOverride(ser, mode, pin):
    com.sendMessage(ser, f"ov{mode}{pin}")
    print(com.receiveMessage(ser))

if __name__ == "__main__":
    setPosition(0)