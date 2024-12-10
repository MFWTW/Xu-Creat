import cv2 as cv
import numpy as np



def  right_and_left(img):
    counters,_=cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for counter in counters:
        if cv.contourArea(counter)>800:
            rect=cv.minAreaRect(counter)
            center= rect[0]
            width,hight=int(rect[1][0]),int(rect[1][1])
            angel=rect[2]
            # cv2.minAreaRect()
            #  函数计算给定轮廓的最小内接矩形。
            # 这个矩形可能不是轴对齐的，
            # 其返回值是一个包含以下元素的元组 
            # (center_x, center_y, width, height, angle)：
            box = cv.boxPoints(rect)
            box = box.astype(np.int32)  # 将角点转换为整数
            cv.drawContours(img, [box], 0, (0,0,0), 2)  # 绘制矩形
            x,y=int(center[0]),int(center[1])
            cv.circle(img, (x,y), 5, (0,0,0), -1)

            return x,y
        else:
            return None,None


