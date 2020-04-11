import cv2
import numpy as np
import os
import sys
from sklearn import svm
from sklearn import preprocessing
import pickle


def sortImgByNumberOfActivePixels(elem):
    return elem[1]


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

    return True

basedirretrain='KittiSeg_2019_04_02_09.56'

dir_test = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\dataset_Olinda_varHeading_fov90\\teste2\\';
dir_segmented = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\RUNS\\'+basedirretrain+'\\results\\';
path_retraindataset = 'C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\data\\data_road\\training\\'
dir_retraindataset = 'image_4retrain'
dirpath = 'RUNS\\'+basedirretrain