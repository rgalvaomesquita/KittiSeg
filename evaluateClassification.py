# -*- Coding: UTF-8 -*-
#coding: utf-8
import evaluationClass_tools as evTools


classes = evTools.ClassesDef.PAVED_NONPAVED

resFile = open('RUNS\\retrain_SVM_balanced_novo_1\\results.txt','r', encoding="utf8")
#resFile = open('RUNS\\retrain_SVM_triang_0\\results.txt','r', encoding="utf8")
#resFile = open('RUNS\\sort2_KittiSeg_2018_11_03_07.43\\results.txt','r', encoding="utf8")


line = resFile.readline()

hit = 0
miss = 0
hitPaved = 0
missPaved = 0
hitRock= 0
missRock = 0
hitNonPaved = 0
missNonPaved = 0
totalPaved = 0
totalNonPaved = 0
totalRock = 0
labelGT = '?'
while line:

	#streetname = line.replace(line.split(' ')[0]+' ','')
	streetname = line.split('[')[0]
	streetname = streetname.replace('\t',' ')

	#label = line.split('[')[1].split(']')[0]
	#numRep = numRepetitionsStreet(streetname) 
	    
	label, npav, nrock, nnonp, avgPavedPx, avgRockPx, avgNonPavedPx = evTools.getNumberOfImagesFromClass(line,classes,0.0)
	
	# if(avgPavedPx <= 0.8 and avgRockPx <= 0.8 and avgNonPavedPx <= 0.8):
	# 	resFileAux = open('RUNS\\KittiSeg_2018_10_17_11.48\\results.txt','r', encoding="utf8")
	# 	lineAux = resFileAux.readline()

	# 	while lineAux:
	# 		streetnameAux = lineAux.replace('\t',' ')
	# 		streetnameAux = streetnameAux.split('[')[0]
			

			
	# 		if streetnameAux == streetname:
	# 			print("LINEAUX")
	# 			print(lineAux)
	# 			label, npav, nrock, nnonp, avgPavedPx, avgRockPx, avgNonPavedPx = evTools.getNumberOfImagesFromClass(lineAux,classes)	
	# 			line = lineAux
	# 			break
	# 		lineAux = resFileAux.readline()
		
	
	gtFile = open('GT_Olinda_id_new.txt','r', encoding="utf8")
	lineGT = gtFile.readline()
	flag = False
	classres = 'None'
	labelGT = '?'
	streetFound = False
	while lineGT:
		
		streetnameGT = lineGT.split('[')[0]
		streetnameGT = streetnameGT.replace('\t',' ')
		#streetnameGT = streetnameGT.split(' ',1)[1]
		
		if streetnameGT == streetname:

			flag = True
			labelGT = lineGT.split(' [')[1].split(']')[0]
			streetFound = True
			

			if classes == evTools.ClassesDef.PAVED_NONPAVED:
				
				if label != '?':
					if labelGT == 'Street' or labelGT == 'Rock':
						totalPaved+=1
					if labelGT == 'Dirt':
						totalNonPaved+=1
				if labelGT != 'Street' and labelGT != 'Rock' and labelGT != 'Dirt' :
					print("aqui: " +streetnameGT)
				if label == 'PAVED' or label == 'ROCK':
					if labelGT == 'Dirt':
				 		miss+=1
				 		missPaved +=1
				 		classres = 'Miss'
				 		
					elif labelGT == 'Street' or labelGT == 'Rock':
				 		hit+=1
				 		hitPaved += 1 
				 		classres = 'Hit'
				 		

				if label == 'NON PAVED':
				 	if labelGT == 'Street' or labelGT == 'Rock':
				 		miss+=1
				 		missNonPaved +=1
				 		classres = 'Miss'
				 		
				 	elif labelGT == 'Dirt':
				 		hit+=1
				 		hitNonPaved += 1
				 		classres = 'Hit'

			elif classes == evTools.ClassesDef.PAVED_NONPAVED_ROCK:

				if labelGT == 'Street':
					totalPaved+=1
				if labelGT == 'Rock':
					totalRock+=1
				if labelGT == 'Dirt':
					totalNonPaved+=1
				if label == 'PAVED':
					if labelGT == 'Street':
						hit+=1
						hitPaved += 1 
						classres = 'Hit'
					else:
						miss+=1
						missPaved += 1 
						classres = 'Miss'
				if label == 'ROCK':
					if labelGT == 'Rock':
						hit+=1
						hitRock += 1 
						classres = 'Hit'
					else:
						miss+=1
						missRock += 1 
						classres = 'Miss'
				if label == 'NON PAVED':
					if labelGT == 'Dirt':
						hit+=1
						hitNonPaved += 1 
						classres = 'Hit'
					else:
						miss+=1
						missNonPaved += 1 
						classres = 'Miss'
			break
        
		
            
		lineGT = gtFile.readline()
	#if labelGT == 'Street' and classres == 'Miss':
	#if(classres == 'Miss'):
		#print("RESFILE")  
		#print('***nome da rua: '+streetname+ ' *** label GT: '+labelGT+' *** label class: '+label+' *** classres: '+classres)
		#print(line)
	#if(streetFound == False):
		#print("rua não encontrada: "+streetname)
	gtFile.close()
	
	flag = False
	classres = ''
	
	line = resFile.readline()
	

resFile.close()
total = hit+miss
print('#Hits: {}'.format(hit))
print('#Misses: {}'.format(miss))
print('#Hit Rate: {}'.format(hit/(total)))

print('#Hits Paved: {}'.format(hitPaved))
print('#Misses Paved: {}'.format(missPaved))
print('#Precision Paved: {}'.format(hitPaved/(hitPaved+missPaved)))
print('#Recall Paved: {}'.format(hitPaved/(totalPaved)))

if classes == evTools.ClassesDef.PAVED_NONPAVED_ROCK:	
	print('#Hits Rock: {}'.format(hitRock))
	print('#Misses Rock: {}'.format(missRock))
	print('#Precision Rock: {}'.format(hitRock/(hitRock+missRock)))
	print('#Recall Rock: {}'.format(hitRock/(totalRock)))

print('#Hits NonPaved: {}'.format(hitNonPaved))
print('#Misses NonPaved: {}'.format(missNonPaved))
print('#Precision NonPaved: {}'.format(hitNonPaved/(hitNonPaved+missNonPaved)))
print('#Recall NonPaved: {}'.format(hitNonPaved/(totalNonPaved)))

