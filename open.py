import cv2 as cv
import numpy as np
from moudle import up_and_down
from moudle import judgement
from moudle import fing
from moudle import my_serial
import time

         
def find(imgtwo1):
    top_img=imgtwo1[0:240,:]
    top_img,num,corners=up_and_down.top(top_img)
    imgtwo1[0:240,:]=top_img
    #under_img=imgtwo1[240:,:]
    #result1,x,y,width,hight=up_and_down.under(under_img)
    #imgtwo1[240:,:]=result1  
    return imgtwo1,num,corners#,x,y,width,hight,corners

vid=cv.VideoCapture(0) 

time.sleep(15)

vid.set(3,640)
vid.set(4,480)


def change_img(img):
     #转换为hsv空间
     hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
     
     #减少亮度
     h,s,v=cv.split(hsv)
     v=cv.subtract(v,50)
     v=np.clip(v,0,255)
     hsv_dark=cv.merge((h,s,v))
     
     #转换为bgr
     darker_image=cv.cvtColor(hsv_dark,cv.COLOR_HSV2BGR)
    
     #转换灰度图
     imggray=cv.cvtColor(darker_image,cv.COLOR_BGR2GRAY)

     #自适应灰度图
     clahe=cv.createCLAHE(clipLimit=2.0,tileGridSize=(15,15))
     equalized=clahe.apply(imggray)
     
     #高斯模糊去噪
     kSize=(11,11)
     imgtwo= cv.GaussianBlur(equalized,kSize, sigmaX=2)

     return imgtwo
while  vid.isOpened:
    sucess,img=vid.read()
    if sucess:
        
        imgtwo=change_img(img)
        
        ret1,imgtwo0=cv.threshold(imgtwo,0,255,cv.THRESH_OTSU+cv.THRESH_BINARY_INV)
        
        kSize = (5, 5)  # 卷积核的尺寸
        kernel = np.ones(kSize, dtype=np.uint8)  # 生成盒式卷积核
        imgtwo1 = cv.morphologyEx(imgtwo0, cv.MORPH_OPEN, kernel)
        
        #识别圆
        '''
        circles,x,y=fing.detect_circle(img,imgtwo1)

        if circles is not None:
            if x==320 and y==240:
                #夹小球
                pass
            else:
                # serial.Serial_Tx(320,240,x,y)
                pass
        else:
        '''
        result,num_corners,corners=find(imgtwo1)
        
        if num_corners>=0 and num_corners<=20 :
            result1=judgement.judge0(result,num_corners)
        
        elif num_corners >= 21 and num_corners<=40:
            judgement.judge1(num_corners, result)  # 使用result而不是imgtwo1
    
        if num_corners >=61 and num_corners<=80:
            result1=judgement.judge4(num_corners, result)  # 使用result而不是imgtwo1
          
        if num_corners >=41 and num_corners<=60:           
            result1=judgement.judge2(num_corners,result)
        
        
        if result1 is not None:
            cv.imshow("img", result1)
        else:
            cv.imshow("wuwu")
        if cv.waitKey(1) & 0xFF==ord(' '):
            break
    else:
        break

vid.release()
cv.destroyAllWindows()     
