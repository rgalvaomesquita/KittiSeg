import cv2
import os
import scipy as scp
import scipy.misc
import numpy as np

def triangStats(img, noHoles = False, minPercArea = 0.1):


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

    if (maxArea <= minPercArea * imggray.shape[0] * imggray.shape[1]):
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
                        if (noHoles or (img[i][j][0] != 0 or img[i][j][1] != 0 or img[i][j][2] != 0)):
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

    #desc = [maxArea / triangleArea, 0 if v3y - v1y == 0 else (v2y - v1y) / (v3y - v1y),
            #1 if v1x - v2x > 0 and v3x - v1x > 0 else 0, np.rad2deg(np.arctan( abs(v3y-v2y) / (v3x - v2x)))]
    if triangleArea == 0 or (v3x - v2x) == 0:
        return False, None, None, None, None
    desc = [contActivePixels/triangleArea, np.rad2deg(np.arctan(abs(v3y - v2y) / (v3x - v2x))), 1 if v1x - v2x > 0 and v3x - v1x > 0 else 0 ]
    return True, np.array([desc]),contActivePixels/(imggray.shape[0] * imggray.shape[1]), imgCnt, color
