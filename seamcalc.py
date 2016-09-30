from skimage import filters
import numpy as np

def energyGradient(image):
    energyMatrix = image.convert('L')
    energyMatrix = filters.sobel(energyMatrix)
    (height, width) = energyMatrix.shape
    for i in range(0, height):
        energyMatrix[i,0] = energyMatrix[i,1]
        energyMatrix[i,width-1] = energyMatrix[i,width-2]
    for i in range(0, width):
        energyMatrix[0,i] = energyMatrix[1,i]
        energyMatrix[height-1,i] = energyMatrix[height-2,i]
    return energyMatrix

def calculateSeam(energy):
    seamEnergy = np.zeros(energy.shape)
    seamDirection = np.zeros(energy.shape, dtype=np.int)
    (height, width) = energy.shape
    for i in range(0, width):
        seamEnergy[0,i] = energy[0, i]
    for i in range(1, height):
        for j in range(0, width):
            if j > 0 and seamEnergy[i-1, j-1] < seamEnergy[i-1, j] and (j == width-1 or seamEnergy[i-1, j-1] <= seamEnergy[i-1,j+1]):
                seamEnergy[i,j] = energy[i,j] + seamEnergy[i-1,j-1]
                seamDirection[i,j] = -1
            elif j == width-1 or seamEnergy[i-1,j] <= seamEnergy[i-1,j+1]:
                seamEnergy[i, j] = energy[i, j] + seamEnergy[i - 1, j]
            else:
                seamEnergy[i, j] = energy[i, j] + seamEnergy[i - 1, j + 1]
                seamDirection[i, j] = 1
    return seamEnergy, seamDirection
