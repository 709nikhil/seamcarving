from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import sys
import seamcalc

def seamTrace(lowestSeam, seamDirection, pixelsToRemove):
    (height, width) = seamDirection.shape
    j = lowestSeam
    for i in reversed(range(0, height)):
        pixelsToRemove[i,j] = 1
        j += seamDirection[i, j]
    return pixelsToRemove


def findLowestSeam(seamEnergy, seamDirection):
    pixelsToRemove = np.zeros(seamEnergy.shape, dtype=np.int)
    (height, width) = seamEnergy.shape
    lowestSeam = np.argmin(seamEnergy[height-1,:])
    pixelsToRemove = seamTrace(lowestSeam, seamDirection, pixelsToRemove)
    return pixelsToRemove


def removeSeam(image, energyMatrix, seamEnergy, seamDirection):
    pixelsToRemove = findLowestSeam(seamEnergy, seamDirection)
    (width, height) = image.size
    #(height, width, _) = image.shape
    newImage = np.zeros((height, width-1, 3), dtype=np.uint8)
    newEnergyMatrix = np.zeros((height, width-1))
    for i in range(0, height):
        k = 0
        for j in range(0, width):
            if pixelsToRemove[i,j] == 1:
                continue
            #newImage[i,k,:] = image[i,j,:]
            newImage[i, k, :] = image.getpixel((j,i))
            newEnergyMatrix[i,k] = energyMatrix[i,j]
            k += 1
    return newImage, newEnergyMatrix


image = Image.open(sys.argv[1])
newWidth = int(sys.argv[2])

(width,height) = image.size
newImage = image
#newImage = np.array(image)
for i in range(0, width - newWidth):
    energyMatrix = seamcalc.energyGradient(newImage)
    seamEnergy, seamDirection = seamcalc.calculateSeam(energyMatrix)
    newImage, energyMatrix = removeSeam(newImage, energyMatrix, seamEnergy, seamDirection)
    newImage = Image.fromarray(newImage)
    print i
#plt.imshow(newImage)
#plt.show()
newImage.save('resized.jpg')
