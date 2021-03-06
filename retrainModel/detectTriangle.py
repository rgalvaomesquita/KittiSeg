import cv2
import numpy as np
import os
import sys
from sklearn import svm
from sklearn import preprocessing
import pickle


def triangStats(img):
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, imbw = cv2.threshold(imggray, 10, 255, 0)
    _, contours, _ = cv2.findContours(imbw, 1, 2)

    maxArea = 0;
    Ax = Ay = Bx = By = Cx = Cy = 0
    areaCnt = 0
    maxCnt = None
    idx = -1
    for cnt in contours:
        idx += 1
        retval, triangle = cv2.minEnclosingTriangle(cnt)
        if (triangle is None):
            continue
        areaCnt = cv2.contourArea(cnt)
        if (areaCnt <= maxArea):
            continue
        maxArea = areaCnt
        maxCnt = idx
        Ax = triangle[0][0][0]
        Ay = triangle[0][0][1]

        Bx = triangle[1][0][0]
        By = triangle[1][0][1]

        Cx = triangle[2][0][0]
        Cy = triangle[2][0][1]

    if (maxArea < 0.1 * imggray.shape[0] * imggray.shape[1]):
        return False, None, None, None, None
    v1x = 0
    v1y = 0
    v2x = 0
    v2y = 0
    v3x = 0
    v3y = 0
    imgCnt = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    mask = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    cv2.drawContours(mask, contours, maxCnt, color=(255, 255, 255), thickness=cv2.FILLED)
    color = [0, 0, 0]
    contActivePixels = 0
    valret = True
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if (mask[i, j, 0] == 255 and mask[i, j, 1] == 255 and mask[i, j, 2] == 255):
                if(img[i, j, 0] != 0 or img[i, j, 1] != 0 or img[i, j, 2] != 0):
                    contActivePixels+=1
                if (color[0] == 0 and color[1] == 0 and color[2] == 0):
                    color[0] = int(img[i][j][0])
                    color[1] = int(img[i][j][1])
                    color[2] = int(img[i][j][2])
                else:
                    if (img[i][j][0] != color[0] or img[i][j][1] != color[1] or img[i][j][2] != color[2]):
                        valret = False

    if(valret == False):
        return False, None, None, None, None

    cv2.drawContours(imgCnt, contours, maxCnt, color=color, thickness=cv2.FILLED)

    if (Cy < By and Cy < Ay):
        v1y = Cy
        v1x = Cx
        if (Ax < Bx):
            v2x = Ax
            v2y = Ay
            v3x = Bx
            v3y = By
        else:
            v2x = Bx
            v2y = By
            v3x = Ax
            v3y = Ay
    elif (By < Cy and By < Ay):
        v1y = By
        v1x = Bx
        if (Ax < Cx):
            v2x = Ax
            v2y = Ay
            v3x = Cx
            v3y = Cy
        else:
            v2x = Cx
            v2y = Cy
            v3x = Ax
            v3y = Ay
    else:
        v1y = Ay
        v1x = Ax
        if (Bx < Cx):
            v2x = Bx
            v2y = By
            v3x = Cx
            v3y = Cy
        else:
            v2x = Cx
            v2y = Cy
            v3x = Bx
            v3y = By

    # (x,y),radius = cv2.minEnclosingCircle(cnt)
    triangleArea = abs((v2x * (v1y - v3y) + v1x * (v3y - v2y) + v3x * (v2y - v1y)) / 2)
    # print(f"({v1x},{v1y}) ({v2x},{v2y}) ({v3x},{v3y}) {maxArea} {triangleArea}")
    # a=input('pare')
    # center = (int(x),int(y))
    # radius = int(radius)
    # cv2.circle(img,center,radius,(255,255,0),2)

    descant = [maxArea/triangleArea,0 if v3y-v1y==0 else (v2y-v1y)/(v3y-v1y),1 if v1x-v2x > 0 and v3x-v1x > 0 else 0]
    desc = [contActivePixels/triangleArea, np.rad2deg(np.arctan(abs(v3y - v2y) / (v3x - v2x))), 1 if v1x - v2x > 0 and v3x - v1x > 0 else 0 ]
    return True, np.array([desc]), imgCnt, color, np.array([descant])






clf = svm.SVC(kernel='linear')

inputdir = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\data_road\\training\\gt_image_4_semlateral\\"
inputdirbad = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\retrainModel\\badtriang_go\\"
inputdirgood = "C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\retrainModel\\goodtriang_go\\"





all_desc = None
labels = []

for streetname in os.listdir(inputdir):
    img = cv2.imread(f"{inputdir}{streetname}", cv2.IMREAD_COLOR)
        # print(f"{inputdir}{streetname}")

    _, desc, imgCnt, _, descant = triangStats(img)
    print(f"RES: {streetname}:{desc}")
    print(f"RES: {streetname}:{descant}")
    print("**************")
    if (desc is None):
        continue
    if (all_desc is None):
        all_desc = desc
    else:
        all_desc = np.concatenate((all_desc, desc), axis=0)
     #   cv2.imwrite(f"badtriang_met2\\{streetname}", imgCnt)
    labels.append(0)

    # if( desc[0][0]>0.8 and desc[0][1] > 0.9 and desc[0][1] < 1.1 and desc[0][2] == 1):
    #     print(f"GOOD: {streetname}:{desc}")
    #     cv2.imwrite(f"goodtriang_apague\\{streetname}",imgCnt)
    #     labels.append(1)
    # else:
    #     cv2.imwrite(f"badtriang_apague\\{streetname}", imgCnt)
    #     print(f"BAD: {streetname}:{desc}")
    #     labels.append(0)

a=input('pare')
for streetname in os.listdir(inputdirgood):
    img = cv2.imread(f"{inputdirgood}{streetname}",cv2.IMREAD_COLOR)
    #print(f"{inputdir}{streetname}")


    _,desc,imgCnt,_ = triangStats(img)
    if(desc is None):
        continue
    if(all_desc is None):
        all_desc = desc
    else:
        all_desc = np.concatenate((all_desc,desc),axis=0)
    #cv2.imwrite(f"goodtriang_met2\\{streetname}", imgCnt)
    labels.append(1)

for streetname in os.listdir(inputdirbad):
    img = cv2.imread(f"{inputdirbad}{streetname}", cv2.IMREAD_COLOR)
        # print(f"{inputdir}{streetname}")

    _, desc, imgCnt, _ = triangStats(img)
    if (desc is None):
        continue
    if (all_desc is None):
        all_desc = desc
    else:
        all_desc = np.concatenate((all_desc, desc), axis=0)
     #   cv2.imwrite(f"badtriang_met2\\{streetname}", imgCnt)
    labels.append(0)
    # if( desc[0][0]>0.8 and desc[0][1] > 0.9 and desc[0][1] < 1.1 and desc[0][2] == 1):
    #         print(f"GOOD: {streetname}:{desc}")
    #         cv2.imwrite(f"goodtriang_met2\\{streetname}",imgCnt)
    #         labels.append(1)
    # else:
    #     cv2.imwrite(f"badtriang_met2\\{streetname}", imgCnt)
    #     print(f"BAD: {streetname}:{desc}")
    #     labels.append(0)
    #
scaler = preprocessing.MinMaxScaler()
#
# print(f"descAll: {all_desc}")
print(scaler.fit(all_desc))
all_desc=scaler.transform(all_desc)
# print(f"descAll pre proc: {all_desc}")
clf.fit(all_desc,labels)
#

# print(desctrue)
# desctrue_sc=scaler.transform(desctrue)
# print(desctrue_sc)

#
# print(descfalse)
# descfalse_sc=scaler.transform(descfalse)
# print(descfalse)
#
# print(clf.predict(desctrue_sc))
# print(clf.predict(descfalse_sc))
# print(len(labels))
#
filename = 'svm_model3.sav'
pickle.dump(clf, open(filename, 'wb'))
#
filenameScaler = 'scaler3.sav'
pickle.dump(scaler, open(filenameScaler, 'wb'))
#
loaded_scaler = pickle.load(open(filenameScaler, 'rb'))
#
loaded_model = pickle.load(open(filename, 'rb'))

img_true = cv2.imread(f"{inputdirgood}-7.9616_-34.8554_heading=-1.png",cv2.IMREAD_COLOR)
_,desctrue,img2,_ = triangStats(img_true)
img_false = cv2.imread(f"{inputdirbad}-7.96459_-34.851980000000005_heading=45.png",cv2.IMREAD_COLOR)
_,descfalse,img2,_ = triangStats(img_false)
print(loaded_model.predict(loaded_scaler.transform(desctrue)))
print(loaded_model.predict(loaded_scaler.transform(descfalse)))
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
# print(desctrue_sc)
# print(loaded_scaler.transform(desctrue))
# print(descfalse_sc)
# print(loaded_scaler.transform(descfalse))