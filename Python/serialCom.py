import serial
import time
import serial.serialutil
from globals import PROJPATH

# Replace 'COM3' with the port name your Arduino is connected to
port = 'COM3'
# baudrate = 921600
# baudrate = 115200
# baudrate = 1000000
baudrate = 2000000

def openPort():
    try:
        print("Connecting...")
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)
        print(f'Connected to {port} at {baudrate} baud rate')
    except UnboundLocalError:
        print("serial couldnt be found mb arduino is not connected?")
        return False
    except Exception as e:
        print(e)
        return False
    else:
        return ser

def closePort(ser):
    try:
        if (serial):
                ser.close()
                print('Serial port closed')
    finally: pass
    # except AttributeError as e:
    #     print("Could not connect. Maybe serial port is occupied.")

def capturePartial(ser, name, instruction = "cpt"):
    """Capture image without starting new connection
    Returns:
    bool: whether the capture was successfull"""

    try:
        sendMessage(ser, instruction)

        with open(f"{PROJPATH}imgs/img{name}.jpeg", "wb") as f:
            # print(f)
            prev_byte = 0x00
            while True:
                # print(ser.in_waiting)
                if ser.in_waiting > 0:
                    bytes = ser.read()
                    byte = bytes[0]
                    f.write(bytes)
                    if byte == 0xD9 and prev_byte == 0xFF:
                        print("Capture done")
                        f.close()
                        break
                    prev_byte = byte
                    # print(byte)
    except serial.SerialException as e:
        print(f'Error: {e}')
        return False
    except AttributeError:
        print("Could not read data, maybe serial port is occupied?")
        return False
    except KeyboardInterrupt:
        print('Program interrupted')
        return False
    else:
        return True


def captureSingle(name):
    """Capture image and take care of serial connection
    Returns:
    bool: whether the capture was successfull"""
    ser = openPort()
    status = capturePartial(ser, name)
    closePort(ser)
    return status

def sendMessage(ser, msg):
    """Send a string to arduino via serial port"""
    try:
        if ser == False:
            raise serial.serialutil.PortNotOpenError
        else:
            ser.write(bytes(msg, "utf-8"))
            time.sleep(0.05)
    except serial.serialutil.PortNotOpenError:
        print("Error: Port is not open")

def receiveMessage(ser, timeout = 5):
    """Read and return a string from the serial port"""
    # ser.timeout = timeout
    try:
        data = ser.readline().decode().rstrip()
    except UnicodeDecodeError:
        print("problem with decoding msg, using alternative method")
        data = ser.readline().decode('latin-1').rstrip()
    except serial.serialutil.PortNotOpenError:
        print("Error: Port is not open")

    if data == None:
        print("(Receive) No message from arduino received :(")
    else: 
        return data
    
def waitForMessage(ser, msg, timeout = 5):
    """Read from the serial port until a specific message has been received"""
    # ser.timeout = timeout This isnt working for some reason
    try:
        data = ser.read_until(msg).decode().rstrip()
    except serial.serialutil.PortNotOpenError and AttributeError:
        print("Error: Port is not open")

    if data == None:
        print("(Wait) No message from arduino received :(")
    else: 
        return data

if __name__ == "__main__":
    captureSingle(0)
    # closePort(ser)
    # ser.write(b"hello")
    # ser = openPort()
    # sendMessage(ser, "on")
    # while True:
    #     msg = input()
    #     if msg == "end": break
    #     sendMessage(ser, msg)
    # print(waitForMessage(ser, "Hello", 10))
    # msg = receiveMessage(ser)
    # print(msg)
    # ser.write(bytes("3", "utf-8"))
    # data = wait
    # closePort(ser)