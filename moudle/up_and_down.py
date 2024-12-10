import cv2 as cv
import numpy as np

def top(top_img):
    #创建副本
    #process_img=top_img.copy()
    # 使用边缘检测

    edges= cv.Canny(top_img, 50, 150)

    # 使用 Shi-Tomasi 算法检测角点
    corners=cv.goodFeaturesToTrack(edges,maxCorners=50,qualityLevel=0.1,minDistance=50)
    if corners is not None and len(corners) > 0:  # 检查是否检测到角点
        count = len(corners)  # 记录角点数量
        corners = np.float32(corners) 
    #精确到亚像素
        criteria=(cv.TERM_CRITERIA_EPS +cv.TERM_CRITERIA_MAX_ITER,30,0.01)
        
        h,w=top_img.shape[:2]
        win_size=(5,5)
        if w >= win_size[0] * 2 + 5 and h >= win_size[1] * 2 + 5:
            corners=cv.cornerSubPix(top_img,corners,win_size,(-1,-1),criteria)
        else:
            print("Warning: Image size too small for cornerSubPix optimization.")
        
            #寻找x，y
            corners = np.reshape(corners,(-1, 2))
            corners=np.int32(corners) 
            for i in range(len(corners)):
                x,y=corners[i]
                cv.circle(top_img, (x, y), 5, (0, 255, 0), 1)
                  
        return top_img,count,corners
    else:
        count=0
        return top_img,count,0 
        

def under(under_img):
    x, y, width, hight= None, None, None, None
    counters,_=cv.findContours(under_img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    for counter in counters:
        if cv.contourArea(counter)>800:
            rect=cv.minAreaRect(counter)
            center = rect[0]
            print(int(center[0]),int(center[1]))
            width,hight=int(rect[1][0]),int(rect[1][1])
            angel=rect[2]
            # cv2.minAreaRect()
            #  函数计算给定轮廓的最小内接矩形。
            # 这个矩形可能不是轴对齐的，
            # 其返回值是一个包含以下元素的元组 
            # (center_x, center_y, width, height, angle)：
            box = cv.boxPoints(rect)
            box = box.astype(np.int32)  # 将角点转换为整数
            cv.drawContours(under_img, [box], 0, (0,0,0), 2)  # 绘制矩形
            x,y=int(center[0]),int(center[1])
            cv.circle(under_img, (x,y), 5, (0,0,0), -1)
            break

    if all(v is not None for v in [x,y,width,hight] ):

        return under_img,x,y,width,hight
    else:
        return under_img, None, None, None, None
