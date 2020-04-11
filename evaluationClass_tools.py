import cv2
import os
import numpy as np
import scipy as scp
import scipy.misc

from enum import Enum
class ClassesDef(Enum):
     PAVED_NONPAVED = 1
     PAVED_NONPAVED_ROCK = 2

#classes = ClassesDef.PAVED_NONPAVED_ROCK



def good_res_image(img):

	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

	imgbw = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)[1]  # ensure binary
	ret, labels = cv2.connectedComponents(imgbw)
	
	

	countCCPixels = np.zeros(ret, dtype=int)
	rows,cols = labels.shape[:2]
	

	if len(countCCPixels) == 2:
		for i in range(rows):
	 		for j in range(cols):
	 			if not (img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 0): 
	 				countCCPixels[labels[i][j]] = countCCPixels[labels[i][j]] + 1
	 				if countCCPixels[labels[i][j]] >= rows*cols*0.1:
	 					return True
		#if countCCPixels[0] >= rows*cols*0.1 and countCCPixels[1] >= rows*cols*0.1 :
	 		#return True
	return False

    
	
	
	# for i in range(len(countCCPixels)):
		
	# 	if countCCPixels[i] >= rows*cols/4.0:
	# 		return True

	# return False

def alreadyAnalysedImg(img, analysed_images):
	
	for analysed_image in analysed_images:
		width, height, z = analysed_image.shape
		flagNextImg = False
		flagAlreadyAnalysed = True
		for i in range(width):
			for j in range(height):
				if analysed_image[i,j,0] != img[i,j,0] or analysed_image[i,j,1] != img[i,j,1] or analysed_image[i,j,2] != img[i,j,2]:
					flagNextImg = True
					flagAlreadyAnalysed = False
					break
			if flagNextImg:
				break
		if flagAlreadyAnalysed:
			return True

	return False

# def saveStreet(street):

# 	if street[len(street)-1] == ' ':
# 		street = street[0:len(street)-1]

# 	streetpath_input = os.path.join(maindir,street)
	
# 	os.makedirs(os.path.join(dest_dir,street), exist_ok=True)
# 	analysed_images = []
# 	for imgName in os.listdir(maindir+''+street):
		

# 		input_image = os.path.join(streetpath_input,imgName)
		
# 		image = scipy.misc.imread(input_image, mode='RGB')

# 		if alreadyAnalysedImg(image, analysed_images):
# 			continue

		
# 		analysed_images.append(image)
# 		scipy.misc.imsave(os.path.join(os.path.join(dest_dir,street),imgName), image)


def numRepetitionsStreet(street):

	if street[len(street)-1] == ' ':
		street = street[0:len(street)-1]

	streetpath_input = os.path.join(maindir,street)
	numRep = 0
	analysed_images = []

	for imgName in os.listdir(maindir+''+street):
		

		input_image = os.path.join(streetpath_input,imgName)
		
		image = scipy.misc.imread(input_image, mode='RGB')


		if alreadyAnalysedImg(image, analysed_images):
			numRep = numRep + 1
			continue

		
		analysed_images.append(image)

	return numRep

def getNumberOfImagesFromClass(line, classes, u):
	if len(line.strip()) == 0 :
		return '?', 0, 0, 0, 0, 0, 0
	numImgs = int(line.split('number of images: ')[1].split(' number')[0])
	#print(numImgs)

	numPavedImgs = int(line.split('number of paved images: ')[1].split(' number')[0])

	numRockImgs = int(line.split('number of rock images: ')[1].split(' number')[0])

	numNonPavedImgs = int(line.split('number of non-paved images: ')[1].split(' average')[0])

	avgPavedPx = float(line.split('average paved pixels: ')[1].split(' average')[0])
	
	avgRockPx = float(line.split('average rock pixels: ')[1].split(' average')[0])
	
	avgNonPavedPx = float(line.split('average non-paved pixels: ')[1])
	
	#print('{} {} {} {}'.format(numImgs, numPavedImgs, numRockImgs, numNonPavedImgs))
	#print(numNonPavedImgs)
	total = numPavedImgs + numRockImgs + numNonPavedImgs
	#if numRep > 6*abs(numPavedImgs + numRockImgs - numNonPavedImgs):
		#print(streetname)
		#print("Rep: {}".format(numRep))
		#print("dif: {}".format(abs(numPavedImgs + numRockImgs - numNonPavedImgs)))
		#saveStreet(streetname)
	if numPavedImgs +numNonPavedImgs+numRockImgs == 0 or abs(numPavedImgs + numRockImgs - numNonPavedImgs) < u*(numPavedImgs + numRockImgs + numNonPavedImgs):
		return '?' , numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
	
	
	if classes == ClassesDef.PAVED_NONPAVED:
		if numPavedImgs + numRockImgs > numNonPavedImgs:
			return 'PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
		else:
			return 'NON PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx

	if classes == ClassesDef.PAVED_NONPAVED_ROCK:		
		if numPavedImgs > numNonPavedImgs and numPavedImgs > numRockImgs:
			return 'PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
		if numNonPavedImgs > numPavedImgs and numNonPavedImgs > numRockImgs:
			return 'NON PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
		if numRockImgs > numNonPavedImgs and numRockImgs > numNonPavedImgs:
			return 'ROCK', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx


		if numPavedImgs + numRockImgs > numNonPavedImgs:
			if numRockImgs >= numPavedImgs:
				return 'ROCK', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
			else:
				return 'PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
		else:
			return 'NON PAVED', numPavedImgs, numRockImgs, numNonPavedImgs, avgPavedPx, avgRockPx, avgNonPavedPx
	