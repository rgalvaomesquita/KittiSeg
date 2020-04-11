import cv2
import os
import scipy as scp
import scipy.misc
import matplotlib
from sklearn.cluster import KMeans
import numpy as np
import evaluationClass_tools as evTools
import random
from sklearn import svm
from sklearn import preprocessing
import pickle

import triangle_detection as triang

def oneClass(image_seg):
    rows, cols = image_seg.shape[:2]

    color = [0, 0, 0]
    for i in range(rows):
        for j in range(cols):
            if (image_seg[i][j][0] == 0 and image_seg[i][j][1] == 0 and image_seg[i][j][2] == 0):
                continue
            else:
                if (color[0] == 0 and color[1] == 0 and color[2] == [0]):
                    color[0] = image_seg[i][j][0]
                    color[1] = image_seg[i][j][1]
                    color[2] = image_seg[i][j][2]
                    continue
                if (image_seg[i][j][0] != color[0] or image_seg[i][j][1] != color[1] and image_seg[i][j][2] != color[2]):
                    return False

    return True, color

# def triangStats(img, singleColor = True):
#     imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, imbw = cv2.threshold(imggray, 10, 255, 0)
#     _, contours, _ = cv2.findContours(imbw, 1, 2)

#     maxArea = 0;
#     Ax = Ay = Bx = By = Cx = Cy = 0
#     areaCnt = 0
#     maxCnt = None
#     idx = -1
#     for cnt in contours:
#         idx += 1
#         retval, triangle = cv2.minEnclosingTriangle(cnt)
#         if (triangle is None):
#             continue
#         areaCnt = cv2.contourArea(cnt)
#         if (areaCnt <= maxArea):
#             continue
#         maxArea = areaCnt
#         maxCnt = idx
#         Ax = triangle[0][0][0]
#         Ay = triangle[0][0][1]

#         Bx = triangle[1][0][0]
#         By = triangle[1][0][1]

#         Cx = triangle[2][0][0]
#         Cy = triangle[2][0][1]

#     if (maxArea < 0.1 * imggray.shape[0] * imggray.shape[1]):
#         return False, None, None, None
#     v1x = 0
#     v1y = 0
#     v2x = 0
#     v2y = 0
#     v3x = 0
#     v3y = 0
#     imgCnt = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
#     mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
#     cv2.drawContours(mask, contours, maxCnt, color=(255, 255, 255), thickness=cv2.FILLED)
#     color = [0, 0, 0]
#     contActivePixels = 0
#     valret = True
#     for i in range(mask.shape[0]):
#         for j in range(mask.shape[1]):
#             if (mask[i, j, 0] == 255 and mask[i, j, 1] == 255 and mask[i, j, 2] == 255):
#                 if(img[i, j, 0] != 0 or img[i, j, 1] != 0 or img[i, j, 2] != 0):
#                     contActivePixels+=1
#                 if (color[0] == 0 and color[1] == 0 and color[2] == 0):
#                     color[0] = int(img[i][j][0])
#                     color[1] = int(img[i][j][1])
#                     color[2] = int(img[i][j][2])
#                 else:
#                     if (img[i][j][0] != color[0] or img[i][j][1] != color[1] or img[i][j][2] != color[2]):
#                         valret = False

#     if(singleColor == True and valret == False):
#         return False, None, None, None

#     cv2.drawContours(imgCnt, contours, maxCnt, color=color, thickness=cv2.FILLED)

#     if (Cy < By and Cy < Ay):
#         v1y = Cy
#         v1x = Cx
#         if (Ax < Bx):
#             v2x = Ax
#             v2y = Ay
#             v3x = Bx
#             v3y = By
#         else:
#             v2x = Bx
#             v2y = By
#             v3x = Ax
#             v3y = Ay
#     elif (By < Cy and By < Ay):
#         v1y = By
#         v1x = Bx
#         if (Ax < Cx):
#             v2x = Ax
#             v2y = Ay
#             v3x = Cx
#             v3y = Cy
#         else:
#             v2x = Cx
#             v2y = Cy
#             v3x = Ax
#             v3y = Ay
#     else:
#         v1y = Ay
#         v1x = Ax
#         if (Bx < Cx):
#             v2x = Bx
#             v2y = By
#             v3x = Cx
#             v3y = Cy
#         else:
#             v2x = Cx
#             v2y = Cy
#             v3x = Bx
#             v3y = By

#     # (x,y),radius = cv2.minEnclosingCircle(cnt)
#     triangleArea = abs((v2x * (v1y - v3y) + v1x * (v3y - v2y) + v3x * (v2y - v1y)) / 2)
#     # print(f"({v1x},{v1y}) ({v2x},{v2y}) ({v3x},{v3y}) {maxArea} {triangleArea}")
#     # a=input('pare')
#     # center = (int(x),int(y))
#     # radius = int(radius)
#     # cv2.circle(img,center,radius,(255,255,0),2)

#     #desc = [maxArea / triangleArea, 0 if v3y - v1y == 0 else (v2y - v1y) / (v3y - v1y),
#             #1 if v1x - v2x > 0 and v3x - v1x > 0 else 0, np.rad2deg(np.arctan( abs(v3y-v2y) / (v3x - v2x)))]
#     desc = [contActivePixels/triangleArea, np.rad2deg(np.arctan(abs(v3y - v2y) / (v3x - v2x))), 1 if v1x - v2x > 0 and v3x - v1x > 0 else 0 ]
#     return True, np.array([desc]), imgCnt, color




def applySmv(desc, svmModel):
	return svmModel.predict(desc)

def sortImgByNumberOfActivePixels(elem):
	return elem[1]

def sortImgByFilledTriangPerc(elem):
	return elem[1]

def allPxDominantStreet(image_seg, avgPavedPx, avgRockPx, avgNonPavedPx, th):
	rows,cols = image_seg.shape[:2]
					
	endLoop = 0
	validNonZeroPx = 0	
	for i in range(rows):
		for j in range(cols):
			if (image_seg[i][j][0] == 0 and image_seg[i][j][1] == 0 and image_seg[i][j][2] == 0):
				continue
			if avgPavedPx >= th:
				if (image_seg[i][j][0] != 0 or image_seg[i][j][1] != 0 or image_seg[i][j][2] != 255):
					return False
				else:
					validNonZeroPx = validNonZeroPx + 1
			if avgRockPx >= th:
				if (image_seg[i][j][0] != 255 or image_seg[i][j][1] != 0 or image_seg[i][j][2] != 0):
					return False
				else:
					validNonZeroPx = validNonZeroPx + 1
			if avgNonPavedPx >= th:
				if (image_seg[i][j][0] != 0 or (image_seg[i][j][1] != 255 and image_seg[i][j][1] != 100) or image_seg[i][j][2] != 0):
					return False
				else:
					validNonZeroPx = validNonZeroPx + 1

	if validNonZeroPx == 0:
		return False, 0
	else:
		return True, validNonZeroPx


file_smv_model = 'svm_model3.sav'
svm_model = pickle.load(open(file_smv_model, 'rb'))
baseGTtrainfile = 'gt_image_4_balanced_train.txt'
baseGTvalfile = 'gt_image_4_balanced_val.txt'
file_scaler = 'scaler3.sav'
scaler = pickle.load(open(file_scaler, 'rb'))

classes = evTools.ClassesDef.PAVED_NONPAVED_ROCK

basedirretrain='retrain_SVM_balanced_novo_1'

dir_test = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_varHeading_fov90\\teste2\\';
dir_segmented = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\RUNS\\'+basedirretrain+'\\results\\';
path_retraindataset = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\data_road\\training\\'
dir_retraindataset = 'image_4retrain'
dir_gt_retraindataset = 'retrain_SVM_balanced_novo'
dirpath = 'RUNS\\'+basedirretrain

txt_retrain_name = 'retrain_SVM_balanced_novo_2_train.txt'
txt_val_retrain_name = 'retrain_SVM_balanced_novo_2_val.txt'
txtBestResults = 'retrain_SVM_balanced_novo_updatedResults.txt';
firstRetrain = False
try:
    fileBestResults = open(txtBestResults, 'r')
except IOError:
	firstRetrain = True
	fileBestResults = open(txtBestResults, 'w')
	fileBestResults.close()
	fileBestResults = open(txtBestResults, 'r')

fileBestResults.close()
newBestResults = []

resFile = open(os.path.join(dirpath,'results.txt'),'r', encoding="utf8")

line = resFile.readline()



labelGT = '?'
count = 0
streetsPaved = []
streetsRock = []
streetsNP = []


while line:


	streetname = line.replace('\t',' ')
	streetname = streetname.split(' [')[0]
	print('PROCESSING STREET: '+streetname)
	
	th = 0.99

	fileBestResults = open(txtBestResults, 'r')
	lineBestResult = fileBestResults.readline()
	newLineBestResult = line
	bestResultUpdated = False
	
	while lineBestResult:
		streetnameBestResult = lineBestResult.replace('\t',' ')
		streetnameBestResult = streetnameBestResult.split(' [')[0]

		if streetname == streetnameBestResult:
			break
		lineBestResult = fileBestResults.readline()

	fileBestResults.close()


	# label, npav, nrock, nnonp, avgPavedPx, avgRockPx, avgNonPavedPx = evTools.getNumberOfImagesFromClass(line,classes,0)
	# labelBR, npavBR, nrockBR, nnonpBR, avgPavedPxBR, avgRockPxBR, avgNonPavedPxBR = evTools.getNumberOfImagesFromClass(lineBestResult,classes,0)
	# print(lineBestResult)
	
	# if (avgPavedPxBR >= th and avgPavedPxBR > avgPavedPx) or (avgRockPxBR >= th and avgRockPxBR > avgRockPx) or (avgNonPavedPxBR >= th and avgNonPavedPxBR >= avgNonPavedPx):
	# 	newLineBestResult = lineBestResult

	# if avgNonPavedPx < th and avgRockPx < th and avgPavedPx < th and avgNonPavedPxBR < th and avgRockPxBR < th and avgPavedPxBR < th:
	# 	line = resFile.readline()
	# 	newBestResults.append(newLineBestResult)
	# 	continue

	streetpath_test = os.path.join(dir_test,streetname)	
	streetpath_seg = os.path.join(dir_segmented,streetname)
	for filename in os.listdir(streetpath_test):
				
		
		filename_seg = filename.replace('.png','_raw.png');
		
		# print(filename_seg)

		dirToSaveResult = path_retraindataset+dir_gt_retraindataset+'\\'+streetname+'\\';
		# currentImgForegPix = 0
		# BRimgForegPix = 0
		# try:	
		# 	current_image_seg =  scp.misc.imread(streetpath_seg+'\\'+filename_seg,mode='')

		# 	if avgNonPavedPx < th and avgRockPx < th and avgPavedPx < th:
		# 		currentimgOK = False
		# 		print('currentimgok = -false')
		# 	else:
		# 		currentimgOK, currentImgForegPix = allPxDominantStreet(current_image_seg, avgPavedPx, avgRockPx, avgNonPavedPx, th)
		# 		#currentimgOK = currentimgOK and evTools.good_res_image(current_image_seg)
		# 		print('currentimgok = '+str(currentimgOK))
				
		# except Exception as e:
		# 	print('exc curr: '+ str(e))
		# 	print('error to read curr img: '+os.path.join(streetpath_seg,filename_seg))
		# 	currentimgOK = False

		# try:
		# 	BR_image_seg =  scp.misc.imread(dirToSaveResult+filename_seg,mode='')
		# 	if avgNonPavedPxBR < th and avgRockPxBR < th and avgPavedPxBR < th:
		# 		BRimgOK = False
		# 		print('brimgok = -false')
		# 	else:
		# 		BRimgOK, BRimgForegPix = allPxDominantStreet(BR_image_seg, avgPavedPxBR, avgRockPxBR, avgNonPavedPxBR, th)
		# 		#BRimgOK = BRimgOK and evTools.good_res_image(BR_image_seg)
		# 		print('brimgok = '+str(BRimgOK))
				
		# except Exception as e:
		# 	print('Exc: '+ str(e))
		# 	print('error to read BR: '+os.path.join(dirToSaveResult+filename_seg))
		# 	BRimgOK = False
		
		# if currentimgOK == False and BRimgOK == False:
		# 	print('continue')
		# 	continue

		
		try:	
			current_image_seg =  scp.misc.imread(streetpath_seg+'\\'+filename_seg,mode='')
			currentimgOK = True
		except Exception as e:
			currentimgOK = False

		try:	
			BR_image_seg =  scp.misc.imread(dirToSaveResult+filename_seg,mode='')
			BRimgOK = True
		except Exception as e:
			BRimgOK = False

		perfCurrentImage = 0
		if currentimgOK:
			oneClassContour,descCurrImg, _, curImgTriang, colorCurrImg = triang.triangStats(current_image_seg)
			if(oneClassContour):
				goodCurImg = applySmv(scaler.transform(descCurrImg),svm_model)
				if(goodCurImg==1):
					perfCurrentImage = descCurrImg[0][0]
		
		perfBRImage = 0
		if BRimgOK:
			oneClassContour, descBRImg,_, brImgTriang, colorBRImg = triang.triangStats(BR_image_seg)
			#goodBRImage = applySmv(scaler.transform(descBRImg),svm_model)
			#if(goodBRImage==1):
			perfBRImage = descBRImg[0][0]

		#if avgPavedPx >= th or avgPavedPxBR >= th:
		if perfCurrentImage > perfBRImage:
			if not os.path.exists(dirToSaveResult):
			    os.makedirs(dirToSaveResult)
			print('image updated')
			print('path saved to file:')
			print('training/'+ dir_retraindataset +'/'+streetname+ '/' +filename+ ' '+'training/'+ dir_gt_retraindataset+'/'+streetname+ '/' +filename_seg+'\n')	
			arr = ['training/'+ dir_retraindataset +'/'+streetname+ '/' +filename+ ' '+'training/'+ dir_gt_retraindataset+'/'+streetname+ '/' +filename_seg+'\n',perfCurrentImage]
			if (colorCurrImg[0] == 255 and colorCurrImg[1] == 0 and colorCurrImg[2] == 0):
				streetsPaved.append(arr)
			elif colorCurrImg[0] == 0 and colorCurrImg[1] == 255 and colorCurrImg[2] == 0:
				streetsNP.append(arr)
			else:
				streetsRock.append(arr)
			scp.misc.imsave(dirToSaveResult+filename_seg, curImgTriang)
		elif BRimgOK:
			arr = ['training/'+ dir_retraindataset +'/'+streetname+ '/' +filename+ ' '+'training/'+ dir_gt_retraindataset+'/'+streetname+ '/' +filename_seg+'\n',perfBRImage]
			if (colorBRImg[0] == 255 and colorBRImg[1] == 0 and colorBRImg[2] == 0):
				streetsPaved.append(arr)
			elif (colorBRImg[0] == 0 and colorBRImg[1] == 255 and colorBRImg[2] == 0):
				streetsNP.append(arr)
			else:
				streetsRock.append(arr)

			#scp.misc.imsave(dirToSaveResult+filename_seg, BR_image_seg)

		
	newBestResults.append(newLineBestResult)
	line = resFile.readline()

	
fileBestResults = open(txtBestResults, 'w')

for l in newBestResults:
	fileBestResults.write(l)

fileBestResults.close()
#trainfile = open(os.path.join(dirpath,'train4_retrainpercsemlateral3.txt'),'a')
#valfile = open(os.path.join(dirpath,'val4_retrainpercsemlateral3.txt'),'a')

trainfile = open(os.path.join(dirpath,txt_retrain_name),'w')
valfile = open(os.path.join(dirpath,txt_val_retrain_name),'w')

with open(baseGTtrainfile) as f:
	for line in f:
		trainfile.write(line)
trainfile.write('\n')
with open(baseGTvalfile) as f:
	for line in f:
		valfile.write(line)
valfile.write('\n')
#streetsPaved.sort(key=sortImgByFilledTriangPerc, reverse=True)
#streetsNP.sort(key=sortImgByFilledTriangPerc, reverse=True)
#streetsRock.sort(key=sortImgByFilledTriangPerc, reverse=True)

print(len(streetsPaved))
print(len(streetsNP))
print(len(streetsRock))

#minClass = min(len(streetsPaved),len(streetsNP))
#minClass = min(minClass,len(streetsRock))

# for i in range(minClass):
# 	if i % 3 != 0:
# 		trainfile.write(streetsPaved[i][0])
		
# 		trainfile.write(streetsNP[i][0])
		
# 		#trainfile.write(streetsRock[i][0])
		
# 	else:
# 		valfile.write(streetsPaved[i][0])
		
# 		valfile.write(streetsNP[i][0])
		
# 		#valfile.write(streetsRock[i][0])





# maxClass = max(len(streetsPaved),len(streetsNP))
# maxClass= max(maxClass,len(streetsRock))
# for i in range(maxClass):
	
# 	if i % 3 != 0:
# 		if i < len(streetsPaved):
# 			trainfile.write(streetsPaved[i][0])
# 			print(f"train paved: {streetsPaved[i][0]}")
# 		if i < len(streetsRock):
# 			trainfile.write(streetsRock[i][0])
# 			print(f"train rock: {streetsRock[i][0]}")
# 		if i < len(streetsNP):
# 			trainfile.write(streetsNP[i][0])
# 			print(f"train nonpaved: {streetsNP[i][0]}")
		
# 	else:
		
# 		if i < len(streetsPaved):
# 			valfile.write(streetsPaved[i][0])
# 			print(f"val paved: {streetsPaved[i][0]}")
# 		if i < len(streetsRock):
# 			valfile.write(streetsRock[i][0])
# 			print(f"val rock: {streetsRock[i][0]}")
# 		if i < len(streetsNP):
# 			valfile.write(streetsNP[i][0])
# 			print(f"val nonpaved: {streetsNP[i][0]}")
		
minClass = min(len(streetsPaved)+len(streetsRock),len(streetsNP))
flagRock = False
ipaved = 0
irock = 0
inonpaved = 0
for i in range(minClass):
	if i % 3 != 0:

		if( i % 2 == 0):
			trainfile.write(streetsNP[inonpaved][0])
			inonpaved += 1
		else:
			if(flagRock == True or ipaved >= len(streetsPaved)):
				trainfile.write(streetsRock[irock][0])
				flagRock = False
				irock += 1
			elif(flagRock == False or irock >= len(streetsRock)):
			    trainfile.write(streetsPaved[ipaved][0])
			    flagRock = True
			    ipaved += 1
		
		
	else:
		if( i % 2 == 0):
			valfile.write(streetsNP[inonpaved][0])
			inonpaved += 1
		else:
			if(flagRock == True or ipaved >= len(streetsPaved)):
				valfile.write(streetsRock[irock][0])
				flagRock = False
				irock += 1
			elif(flagRock == False or irock >= len(streetsRock)):
			    valfile.write(streetsPaved[ipaved][0])
			    flagRock = True
			    ipaved += 1
		
		

		
trainfile.close();
valfile.close();	



