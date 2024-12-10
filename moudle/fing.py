import cv2 as cv
import numpy as np


def detect_circle(img,imgtwo1):
    """
    识别圆环并返回圆心坐标和半径
    """
    # 转为灰度图
    imghsv= cv.cvtColor(img, cv.COLOR_BGR2HSV)
    
    lowerColor=np.array([100,43,46], dtype=np.uint8)
    upperColor=np.array([124,255,255], dtype=np.uint8)
    binary=cv.inRange(imghsv,lowerColor,upperColor)
    binaryinv=cv.bitwise_not(binary)

    Ksize=(11,11)
    imggray0=cv.GaussianBlur(binaryinv,Ksize,sigmaX=2)

    # Hough 圆检测
    circles = cv.HoughCircles(imggray0, cv.HOUGH_GRADIENT, 1, 30, param1=50, param2=30, minRadius=20, maxRadius=100)

    if circles is not None:
        # 圆心和半径
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            x, y, radius = circle
            # 在图像上绘制圆
            cv.circle(imgtwo1, (x, y), radius, (0, 255, 0), 2)
            cv.circle(imgtwo1, (x, y), 2, (0, 0, 255), 3)
    
            return circles,x,y
    else:
        return None,None,None    
