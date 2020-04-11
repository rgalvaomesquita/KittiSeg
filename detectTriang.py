import cv2
import numpy as np

img = cv2.imread("C:\\Pesquisa\\codigos\\KittiSeg_shivam\\KittiSeg\\RUNS\\KittiSeg_2019_04_02_09.56\\results\\Avenida Marcos Freire\\-7.96061_-34.829919999999994_heading=-1_raw.png", cv2.IMREAD_COLOR)
imggray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(imggray, 1, 255, cv2.THRESH_BINARY)
cv2.imshow("Threshold0", threshold)
_, contours, _ = cv2.findContours(threshold, 1,2)

font = cv2.FONT_HERSHEY_COMPLEX

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
    
    x = approx.ravel()[0]
    y = approx.ravel()[1]

    if len(approx) == 3:
        cv2.drawContours(img, [approx], 0, (0,255,255), 5)
        cv2.putText(img, "Triangle", (x, y), font, 1, color=(0,255,255))
    #elif len(approx) == 4:
     #   cv2.drawContours(img, [approx], 0, (0,255,255), 5)
     #  cv2.putText(img, "Rectangle", (x, y), font, 1, color=(0,255,255))
    #elif len(approx) == 5:
    #    cv2.putText(img, "Pentagon", (x, y), font, 1, color=(0,200,255))
    #elif 6 < len(approx) < 15:
    #    cv2.putText(img, "Ellipse", (x, y), font, 1, color=(0,100,255))
    #else:
    #    cv2.putText(img, "Circle", (x, y), font, 1, color=(0,150,25))

cv2.imshow("shapes", img)
cv2.imshow("Threshold", threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()