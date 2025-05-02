import os
import csv
from PIL import Image
import serialCom as com
from globals import *

cropBox = (IMG_X // 2, 0, IMG_X, IMG_Y)
drawDebugDetectedEdge = True
drawDebugAvgLuminance = False
debugColor = (0, 0, 255)

def prepareImg(name = "image", useCrop = False):
    try:
        im = Image.open(f"{PROJPATH}imgs/{name}.jpeg")
        # if its horizontal, rotate 90 degrees
        if im.size[0] > im.size[1]:
            im = im.transpose(Image.Transpose.ROTATE_90)
        # if useCrop is true, we will only use the right half of the img
        if useCrop:
            im = im.crop(cropBox)
        return im
    
    except FileNotFoundError as e:
        print(f"File could not be opened, mb wrong name / path? Name: {name}")
        return False
    
# extract most red pixels in each row
def processImg(img, angle = 0, sampleIndx = 0):
    R, G, B = 0, 1, 2
    X, Y = 0, 1
    # how many pixel rows to iterate over
    step = 1
    # red coeficient treshold, in the future it should be a lot more
    rTrsh = 15
    # white coeficient treshold
    wTrsh = 10
    # black treshold
    bkTrsh = 15

    size = img.size
    src = img
    img = img.load()

    # list to store x coordinate of the most red pixel
    output = [angle]
    # output[0] = angle

    for y in range(0, size[Y], step):
        prevVal = val = (0, 0, 0)
        rX = 0
        totalL = highestL = avgL = 0
        # find the average luminance
        for x in range(size[X]):
            val = img[x, y]
            luminance = (val[R] + val[G] + val[B]) / 3
            totalL = totalL + luminance
        avgL = int(totalL // size[X])

        ## find the best x value for every row
        for x in range(size[X]):
            # val = img[x, y]
            # rCoef = val[R] - ((val[G] + val[B]) // 2)
            # bkCoef = (prevVal[R] + prevVal[G] + prevVal[B]) // 3
            # if rCoef >= rTrsh and bkCoef >= bkTrsh:
            #     rX = x

            
            val = img[x, y]
            luminance = (val[R] + val[G] + val[B]) / 3
            if luminance > highestL and luminance >= wTrsh:
                highestL = luminance
                rX = x

            prevVal = val

        ## AADDITIONAL FILTERING
        # if rX is at the end, set it to 0 bc its not valid
        if rX == size[X] - 1: rX = 0
        if rX < size[X] / 2: rX = 0

        ## DEBUG DRAWS
        # highlight the selected pixels with pure red, IF rX = 0 then its not valid
        if drawDebugDetectedEdge:
            if rX != 0: img[rX, y] = debugColor

        if drawDebugAvgLuminance:
            for x in range(8):
                img[x, y] = (avgL, avgL, avgL)
        # write values to a string array, even invalid ones to prevent deformation
        output.append(rX)

    src.save(f"{PROJPATH}imgs/img{sampleIndx}.jpeg")
    # print(output)
    return output
    # src.show()

#### PROCESS ALL IMGS IN THE CAPTURE FOLDER
def processAll(numSamples, useCrop):
    print("processing imgs...")
    if os.path.exists(OUTPUT_PATH):
        os.remove(f"{PROJPATH}data/output.txt")
    scanData = open(f"{PROJPATH}data/output.txt", "a")

    #process each img
    for sampleIndx in range(numSamples):
        img = prepareImg(f"img{sampleIndx}", useCrop)
        if img:
            angle = (360 / numSamples) * sampleIndx
            # output[sampleIndx] = processImg(img, angle)
            output = processImg(img, angle, sampleIndx)
            scanData.write("\n" + str(output))
    scanData.close()

def runPreview(useCrop = False):
    status = com.captureSingle("prev")
    if status:
        img = prepareImg("imgprev", useCrop)
        processImg(img)
        img.show()

def testProcess(name, useCrop = False):
    img = prepareImg(name)
    processImg(img)
    img.show()

def cleanCapture():
    index = 0
    while True:
        path = f"{PROJPATH}imgs/img{index}.jpeg"
        if os.path.exists(path):
            os.remove(path)
            print(f'Deleted "img{index}"')
            index += 1
        else:
            break
    print(f"Deleted {index} pictures")
    
if __name__ == "__main__":
    # runPreview()
    testProcess("tst")