import cv2
import os
import random

folderGT = 'gt_image_4_balanced'
folderOrig = 'image_4'
dirGT = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\data_road\\training\\' + folderGT +'\\';



trainfile = open('gt_image_4_balanced_train.txt','w')
valfile = open('gt_image_4_balanced_val.txt','w')

streetsPaved = []
streetsRock = []
streetsNP = []

for filename in os.listdir(dirGT):
   #print('training/image_4_semlateral/'+filename+ ' training/gt_image_4_semlateral/'+filename)
    img = cv2.imread(os.path.join(dirGT,filename))
    rows,cols = img.shape[:2]
    flagEnd = False 
    for i in range(rows):
    	for j in range(cols):
    		if(img[i,j,0]==255 and img[i,j,1]==0 and img[i,j,2]==0):
    			arr = 'training/'+ folderOrig +'/' +filename+ ' '+'training/'+ folderGT +'/'+filename+'\n'
    			streetsPaved.append(arr)
    			flagEnd = True
    			break
    		if(img[i,j,0]==0 and img[i,j,1]==0 and img[i,j,2]==255):
    			arr = 'training/'+ folderOrig +'/' +filename+ ' '+'training/'+ folderGT +'/'+filename+'\n'
    			streetsRock.append(arr)
    			flagEnd = True
    			break
    		elif(img[i,j,0]==0 and img[i,j,1]==255 and img[i,j,2]==0):
    			arr = 'training/'+ folderOrig +'/' +filename+ ' '+'training/'+ folderGT +'/'+filename+'\n'
    			streetsNP.append(arr)
    			flagEnd = True
    			break

    	if(flagEnd == True):
    		break

random.shuffle(streetsPaved)
random.shuffle(streetsRock)
random.shuffle(streetsNP)

flagRock = False
iPaved = 0
iRock = 0
iNP = 0
for i in range(len(streetsPaved)+len(streetsRock)+len(streetsNP)):
	if i % 2 != 0:
		if flagRock == False:
			if i % 3 == 0:
				valfile.write(streetsPaved[iPaved])
				print(f"val paved: {streetsPaved[iPaved]}")
			else:
				trainfile.write(streetsPaved[iPaved])
				print(f"train paved: {streetsPaved[iPaved]}")
			iPaved+=1
			flagRock = True
		else:
			if i % 3 == 0:
				valfile.write(streetsRock[iRock])
				print(f"val prock: {streetsRock[iRock]}")
			else:
				trainfile.write(streetsRock[iRock])
				print(f"train rock: {streetsRock[iRock]}")
			iRock+=1
			flagRock = False
	else:
		
		if i % 3 == 0:
			valfile.write(streetsNP[iNP])
			print(f"val nonpaved: {streetsNP[iNP]}")
		else:
			trainfile.write(streetsNP[iNP])
			print(f"train nonpaved: {streetsNP[iNP]}")

		iNP+=1
		
		#valfile.write(streetsRock[i][0])
		
trainfile.close();
valfile.close();	
