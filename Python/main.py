# Tento kód je soukromým vlastnictví
# Pro zbytek programu můžete kontaktovat autora na discord: lukas420skrrr

import serialCom as com
import postProcess as post
import hardware as hw
from globals import *
import time
from PIL import Image
useCrop = False

def fullScan(numSamples, capture = True, move = True):
    startTime = time.time()
    ser = com.openPort()
    if ser != False:
        for sampleIndx in range(numSamples):
            # if this is the last sample, dont move motor bc its useless
            if (sampleIndx + 1) >= numSamples: move = False
            if capture: com.capturePartial(ser, sampleIndx)
            angle = (360 // numSamples) * (sampleIndx + 1)
            if move: hw.setPosition(ser, angle)
        captureTime = time.time()
        post.processAll(numSamples, useCrop)
        # Print time stats
        endTime = time.time()
        totalSpan = endTime - startTime
        captureSpan = round(captureTime - startTime, 1)
        processSpan = round(totalSpan - captureSpan, 1)
        print("ALL DONE!!")
        print(
f"""
Capturing photos took {captureSpan}s, avg {round(captureSpan / numSamples, 2)}s per photo,
processing took {processSpan}s, avg {round(processSpan / numSamples, 2)}s per sample
""")


    else:
        print("Scan could not be completed")

while True:
    try:
        # Get what we want to do
        action = input("\nEnter new action: ")
        action = action.lower()
        action = action.split()
        if len(action) > 0:

            if action[0] == "open":
                ser = com.openPort()

            elif action[0] == "close":
                try:
                    if ser.is_open:
                        com.closePort(ser)
                except AttributeError:
                    print("Could not close, maybe connection isn't open")
                
            elif action[0] == "mov":
                pos = action[1]
                try:                
                    hw.setPosition(ser, int(pos))
                except ValueError: print(f"invalid instruction: {pos}")
                

            else:
                match action[0]:
                    case "help":
                        print(HELPMSG)

                    case "path":
                        print(PROJPATH)

                    case "info":
                        print(INFOMSG)

                    case "crop":
                        if len(action) == 1 or action[1] == "on":
                            useCrop = True
                            print("imgs will be cropped")

                        elif action[1] == "off" :
                            useCrop = False
                            print("imgs will not be cropped")

                    case "good":
                        if len(action) > 1 and action[1] == "job": print("\n^_^")
                
                    case "lon":
                        com.sendMessage(ser, "lon")

                    case "loff":
                        com.sendMessage(ser, "lof")

                    case "ovrd":
                        if len(action) > 2:
                            pin = int(action[1])
                            mode = int(action[2])
                            hw.pinOverride(ser, mode, pin)
                        else: print("missing pin number and mode")

                    case "process":
                        if len(action) > 1:
                            post.testProcess(action[1], useCrop)
                        else: print ("missing image name")

                    case "msg":
                        if len(action) > 1:
                            msg = action[1]
                            com.sendMessage(ser, msg)
                            print(f"sent message: {msg}")

                    case "echo":
                        if len(action) > 1:
                            sent = action[1]
                            com.sendMessage(ser, sent)
                            received = com.receiveMessage(ser)
                            if received == "":
                                print("No response received")
                            else:
                                print(f'"{received}"')

                    case "clear" | "clean":
                        print("Are you sure you want to delete all photos? (y/n)")
                        while True:
                            i = input().lower().replace(" ", "")
                            # if i == "y" or i == "yes":
                            if i:
                                post.cleanCapture()
                                break
                            elif i == "n" or i == "no":
                                break

                    case "prev":
                        post.runPreview(useCrop)

                    case "scan":
                        # process extra instructions
                        if len(action) > 1:
                            match action[1]:
                                case "":
                                    capture, move = True, True
                                case "pic": 
                                    capture = True
                                    move = False
                                case "mov":
                                    capture = False
                                    move = True
                        else: capture, move = True, True

                        # number of samples per roration
                        numSamples = input("How many samples: ")
                        if (numSamples == ""):
                            numSamples = NUM_SMPLS
                        numSamples = int(numSamples)
                        print(f"Using {numSamples} samples")

                        fullScan(numSamples, capture, move)
                    
                    case "quit":
                        quit(0)

    except NameError:
        print("Error: Port is not open")