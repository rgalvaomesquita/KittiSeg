import cv2
import os
import numpy as np
#import scipy as scp
import scipy.misc
import triangle_detection as triang
import psycopg2
                                                                
maindir = "E:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\RUNS\\retrain_SVM_balanced_novo_2\\results\\"
#or_imgs_dir = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_heading-1_noPolylines\\"
or_imgs_dir = "E:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda\\test\\"
txtFileName = "E:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\RUNS\\retrain_SVM_balanced_novo_2\\results2.txt"
flagvarHeading = True
cidade_id = 1


def conecta():
	try:
		conn = psycopg2.connect("dbname='beautycities' user='postgres' host='localhost' password='admin12345'")
	except Exception as e:
		print(e)
		
	

def insereLocationDB(nome_rua, lat, lng, tipo_pav):

	try:
		conn = psycopg2.connect("dbname='beautycities' user='postgres' host='localhost' password='admin12345'")
	except Exception as e:
		print(e)
	cur = conn.cursor()
	try:
		cur.execute("select * from ruas where nome = '{}'".format(nome_rua))
		res = cur.fetchone()
		if (res is None):
			cur.execute("insert into ruas(fk_cidade_id,nome) values('{}','{}')".format(cidade_id,nome_rua))
			conn.commit()
			cur.execute("select * from ruas where nome = '{}'".format(nome_rua))
			res = cur.fetchone()
		cur.execute("insert into locations(lat,lng,id_rua,id_cidade,tipo_pav) values('{}', '{}','{}','{}','{}')".format(lat,lng,res[1],cidade_id,tipo_pav))
		print(lat,lng)
		conn.commit()
		cur.close()
		conn.close()
	except Exception as e:
		print(e)

def updateRuaTipoDB(tipo_pav, nome_rua):

	try:
		conn = psycopg2.connect("dbname='beautycities' user='postgres' host='localhost' password='admin12345'")
	except:
		print("I am unable to connect to the database")

	try:
		cur = conn.cursor()
		cur.execute("update ruas set tipo_pav = '{}' where nome = '{}'".format(tipo_pav,nome_rua))
		conn.commit()
		cur.close()
		conn.close()
	except Exception as e:
		print(e)

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
			




def numberNonBackgroundPixels(img):
	if img is None:
		return 0,0,0
	rows,cols, channels = img.shape
	numPavedPixels = 0
	numNonPavedPixels = 0
	numRockPixels = 0
	
	
	for i in range(rows):
		for j in range(cols):
			
			if img[i][j][0] == 255 and img[i][j][1] == 0 and img[i][j][2] == 0 :
				numPavedPixels += 1
			elif (img[i][j][0] == 0 and img[i][j][1] == 255 and img[i][j][2] == 0) or (img[i][j][0] == 0 and img[i][j][1] == 100 and img[i][j][2] == 0) :
				numNonPavedPixels += 1
			elif img[i][j][0] == 0 and img[i][j][1] == 0 and img[i][j][2] == 255 :
				numRockPixels += 1


	return numPavedPixels, numNonPavedPixels, numRockPixels 


stream = open('blank_image.png', "rb")
bytes = bytearray(stream.read())
numpyarray = np.asarray(bytes, dtype=np.uint8)
blank_image = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
#blank_image = scipy.misc.imread('blank_image.png', mode='RGB')
#blank_image = cv2.imread('blank_image.png',cv2.IMREAD_COLOR)
#conecta()
for street in os.listdir(maindir):
	
	txtfile = open(txtFileName,'a')
	print('Street: '+street+ ' :')
	location = 'start'
	numClassPixelsBestImg = 0
	numPavedImgs = 0
	numNonPavedImgs = 0
	numRockImgs = 0
	currImgclass = ''
	numPavedPixelsBestImg = 0
	numNonPavedPixelsBestImg = 0;
	numRockPixelsBestImg = 0
	avgPavedPx = 0
	avgNonPavedPx = 0
	avgRockPx = 0
	numLocations = 0
	analysed_images = []

	

	for imgName in os.listdir(maindir+''+street):
		
		

		if flagvarHeading == False and imgName.split('heading=')[1] != '-1_raw.png':
			continue

		imgNameOri = imgName.replace('_raw','')
		fullPathImg_ori = or_imgs_dir+''+street+'\\'+imgNameOri
		stream = open(fullPathImg_ori, "rb")
		bytes = bytearray(stream.read())
		numpyarray = np.asarray(bytes, dtype=np.uint8)
		rgbImage_ori = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
		#rgbImage_ori = scipy.misc.imread(fullPathImg_ori, mode='RGB')
		#rgbImage_ori = cv2.imread(fullPathImg_ori,cv2.IMREAD_COLOR)
		

		if alreadyAnalysedImg(rgbImage_ori, analysed_images):
		#	print(imgNameOri)
			continue

		analysed_images.append(rgbImage_ori)

		fullPathImg = maindir+''+street+'\\'+imgName
		
		stream = open(fullPathImg, "rb")
		bytes = bytearray(stream.read())
		numpyarray = np.asarray(bytes, dtype=np.uint8)
		rgbImage = cv2.imdecode(numpyarray, cv2.IMREAD_UNCHANGED)
		#rgbImage = scipy.misc.imread(fullPathImg, mode='RGB')
		#rgbImage = cv2.imread(fullPathImg,cv2.IMREAD_COLOR)
		
		numPavedPixels, numNonPavedPixels, numRockPixels = numberNonBackgroundPixels(rgbImage)
		
		# b= rgbImage.copy();
		# g= rgbImage.copy();
		# r= rgbImage.copy();
		# b[:,:,1]=0
		# b[:,:,2]=0
		# g[:,:,0]=0
		# g[:,:,2]=0
		# r[:,:,0]=0
		# r[:,:,1]=0


		# _, desc, percForPx, _, _ = triang.triangStats(b,False,0)
		# if( desc is None):
		# 	wpaved = 0
		# else:
		# 	wpaved=desc[0][0]
		# numPavedPixels*=wpaved

		# _, desc, percForPx, _, _ = triang.triangStats(g,False,0)
		# if( desc is None):
		# 	wnonpaved = 0
		# else:
		# 	wnonpaved=desc[0][0]
		# numNonPavedPixels *= wnonpaved

		# _, desc, percForPx, _, _ = triang.triangStats(r,False,0)
		# if( desc is None):
		# 	wrock = 0
		# else:
		# 	wrock=desc[0][0]
		# numRockPixels *= wrock

		currLocation = imgName.split('_heading=')[0];
		lat = currLocation.split('_')[0]
		lng = currLocation.split('_')[1]
		if currLocation == location or location == 'start':
			location = currLocation
			#if numNonPavedPixels + numPavedPixels + numRockPixels > numClassPixelsBestImg:
			numClassPixelsBestImg += numNonPavedPixels+numPavedPixels+numRockPixels
			numPavedPixelsBestImg += numPavedPixels
			numNonPavedPixelsBestImg += numNonPavedPixels
			numRockPixelsBestImg += numRockPixels
		else:
			if numPavedPixelsBestImg > 0 or numNonPavedPixelsBestImg > 0 or numRockPixelsBestImg > 0:
				numLocations += 1
				avgPavedPx += numPavedPixelsBestImg
				avgNonPavedPx += numNonPavedPixelsBestImg
				avgRockPx += numRockPixelsBestImg
				# if numPavedPixelsBestImg > numNonPavedPixelsBestImg and numPavedPixelsBestImg > numRockPixelsBestImg:
				# 	numPavedImgs += 1
				# elif numRockPixelsBestImg > numNonPavedPixelsBestImg and numRockPixelsBestImg > numPavedPixelsBestImg:
				# 	numRockImgs += 1
				# elif numNonPavedPixelsBestImg > numPavedPixelsBestImg and numNonPavedPixelsBestImg > numRockPixelsBestImg:
				# 	numNonPavedImgs += 1

				
				if numPavedPixelsBestImg > numNonPavedPixelsBestImg and numPavedPixelsBestImg > numRockPixelsBestImg:
					numPavedImgs += 1
					insereLocationDB(street, lat, lng, 1)
				elif numRockPixelsBestImg > numNonPavedPixelsBestImg and numRockPixelsBestImg > numPavedPixelsBestImg:
					numRockImgs += 1
					insereLocationDB(street, lat, lng, 2)
				elif numNonPavedPixelsBestImg >= (numPavedPixelsBestImg + numRockPixelsBestImg):
					numNonPavedImgs += 1
					insereLocationDB(street, lat, lng, 3)
				else: 
					if numPavedPixelsBestImg > numRockPixelsBestImg:
						numPavedImgs += 1
					else:
						numRockImgs += 1




			location = currLocation
			numClassPixelsBestImg = numNonPavedPixels+numPavedPixels+numRockPixels
			numPavedPixelsBestImg = numPavedPixels
			numNonPavedPixelsBestImg = numNonPavedPixels
			numRockPixelsBestImg = numRockPixels

			
			

	if numPavedPixelsBestImg > 0 or numNonPavedPixelsBestImg > 0 or numRockPixelsBestImg > 0:
		numLocations += 1
		avgPavedPx += numPavedPixelsBestImg
		avgNonPavedPx += numNonPavedPixelsBestImg
		avgRockPx += numRockPixelsBestImg
		if numPavedPixelsBestImg > numNonPavedPixelsBestImg and numPavedPixelsBestImg > numRockPixelsBestImg:
			numPavedImgs += 1
			insereLocationDB(street, lat, lng, 1)
		elif numRockPixelsBestImg > numNonPavedPixelsBestImg and numRockPixelsBestImg > numNonPavedPixelsBestImg:
			numRockImgs += 1
			insereLocationDB(street, lat, lng, 2)
		elif numNonPavedPixelsBestImg > numPavedPixelsBestImg and numNonPavedPixelsBestImg > numRockPixelsBestImg:
			numNonPavedImgs += 1
			insereLocationDB(street, lat, lng, 3)


	
	txtfile.write(street)

	if numLocations > 0:
		avgPavedPx = avgPavedPx/numLocations
		avgNonPavedPx = avgNonPavedPx/numLocations	
		avgRockPx = avgRockPx/numLocations
		total = (avgPavedPx+avgNonPavedPx+avgRockPx)
		avgPavedPx /= total
		avgNonPavedPx /= total
		avgRockPx /= total

	if avgPavedPx == 0 and avgNonPavedPx == 0 and avgRockPx == 0:
		txtfile.write(' [?] ')
		#print('?')
	else:
		if numPavedImgs > numNonPavedImgs and numPavedImgs > numRockImgs:
			txtfile.write(' [PAVED] ')
			updateRuaTipoDB(1,street)
		elif numNonPavedImgs > numPavedImgs and numNonPavedImgs > numRockImgs:	
			txtfile.write(' [NON PAVED] ')
			updateRuaTipoDB(3,street)
		elif numRockImgs > numPavedImgs and numRockImgs > numNonPavedImgs:
			txtfile.write('	[ROCK] ')
			updateRuaTipoDB(2,street)
		else:
			if avgPavedPx > avgNonPavedPx and avgPavedPx > avgRockPx:
				txtfile.write(' [PAVED] ')
				updateRuaTipoDB(1,street)
			elif avgRockPx > avgNonPavedPx:
				txtfile.write(' [ROCK] ')
				updateRuaTipoDB(2,street)
			else:
				txtfile.write(' [NON PAVED] ')
				updateRuaTipoDB(3,street)

	
	txtfile.write(' number of images: {} number of paved images: {} number of rock images: {} number of non-paved images: {} average paved pixels: {} average rock pixels: {} average non-paved pixels: {} \n'.format(numLocations,numPavedImgs,numRockImgs,numNonPavedImgs,avgPavedPx,avgRockPx, avgNonPavedPx))
	txtfile.close()
	