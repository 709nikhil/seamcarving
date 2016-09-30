from PIL import Image
import numpy as np
import sys
import seamcalc

def seamTrace(lowestSeam, seamDirection, pixelsToRemove):
    (height, width) = seamDirection.shape
    j = lowestSeam
    for i in reversed(range(0, height)):
        pixelsToRemove[i,j] += 1
        j += seamDirection[i, j]
    return pixelsToRemove


def findLowestSeam(seamEnergy, seamDirection, pixelsToRemove):
    (height, width) = seamEnergy.shape
    lowestSeam = np.argmin(seamEnergy[height-1,:])
    pixelsToRemove = seamTrace(lowestSeam, seamDirection, pixelsToRemove)
    seamEnergy[height-1, lowestSeam] = 10000.0
    return pixelsToRemove


def addSeams(image, energyMatrix, seamEnergy, seamDirection, numSeams):
    pixelsToRemove = np.zeros(seamEnergy.shape, dtype=np.int)
    for i in range(numSeams):
        pixelsToRemove = findLowestSeam(seamEnergy, seamDirection, pixelsToRemove)
    (width, height) = image.size
    newImage = np.zeros((height, width+numSeams, 3), dtype=np.uint8)
    for i in range(0, height):
        k = 0
        for j in range(0, width):
            if pixelsToRemove[i,j] >= 1:
                for p in range((pixelsToRemove[i,j]+1)/2):
                    diff = np.subtract(image.getpixel((j,i)), image.getpixel((max(j-1,0),i))) / float(int((pixelsToRemove[i,j]+1)/2)+1)
                    newImage[i, k, :] = tuple(np.add(image.getpixel((max(j-1,0),i)), tuple((p+1) * diff)))
                    k += 1
                if pixelsToRemove[i,j] % 2 == 0:
                    newImage[i, k, :] = image.getpixel((j, i))
                    k += 1
                for p in range((pixelsToRemove[i,j]+1)/2):
                    diff = np.subtract(image.getpixel((min(j+1,width-1),i)), image.getpixel((j,i))) / float(int((pixelsToRemove[i,j]+1)/2)+1)
                    tuple(np.add(image.getpixel((j, i)), tuple((p + 1) * diff)))
                    newImage[i, k, :] = tuple(np.add(image.getpixel((j,i)), tuple((p+1) * diff)))
                    k += 1
            else:
                newImage[i, k, :] = image.getpixel((j, i))
                k += 1
    return newImage


image = Image.open(sys.argv[1])
newWidth = int(sys.argv[2])

(width,height) = image.size
newImage = image
energyMatrix = seamcalc.energyGradient(newImage)
seamEnergy, seamDirection = seamcalc.calculateSeam(energyMatrix)
newImage = addSeams(newImage, energyMatrix, seamEnergy, seamDirection, newWidth - width)
newImage = Image.fromarray(newImage)
newImage.save('resized-inc.jpg')
