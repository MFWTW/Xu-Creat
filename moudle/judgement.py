import cv2 as cv
import numpy as np
from moudle import my_serial
import math
from moudle import ri_and_le
from moudle import up_and_down


def cross(a,b,x1,y1):
    x=x1
    y=y1

    dx=y-b
    dy=x-a

    angle_radians = math.atan(dy/dx)
    angle_degrees = math.degrees(angle_radians)


    angle_degrees=int(angle_degrees)

    if angle_degrees<0:
        if abs(angle_degrees)>=30:
            print("2")
            my_serial.Serial_Tx(2,abs(angle_degrees))
        else:
            print("0")
            my_serial.Serial_Tx(0,0)    
    elif angle_degrees>0:
        if angle_degrees>=30:
            print("1")
            my_serial.Serial_Tx(1,angle_degrees)
        else:
            print("0")
            my_serial.Serial_Tx(0,0)
    elif abs(angle_degrees)<30:
        print("0")
        my_serial.Serial_Tx(0,0)

def judge0(result,num_corners):
    print(f"角点数量{num_corners}")
    under_img=result[240:,:]
    under_img,x1,y1,width,hight=up_and_down.under(under_img)
    result[240:,:]=under_img
    if x1 is None and y1 is None:
        x1=320
        y1=300
    
    a=320
    b=240
    
    cross(a,b,x1,y1)
    
    return result

def judge1(num_corners,result):
    print(f"角点数量：{num_corners}")
    under_img=result[240:,:]
    under_img,x,y,width,hight=up_and_down.under(under_img)
    result[240:,:]=under_img
    if x1 is None and y1 is None:
        x=320
        y=300
        
    flag=0
    if flag==0:
        cen_x=x1//2
        cen_y=y1//2
        img_range1=result[50:240,70:200]
        img_range2=result[50:240,440:570] 
        x1,y1=ri_and_le.right_and_left(img_range1)
        
        x2,y2=ri_and_le.right_and_left(img_range2)
        
        if x1 is not None or x2 is None:
            #已经进入圆环直行
            my_serial.Serial_Tx(0,0)
        if x1 is None or x2 is not None:
            #已经进入圆环直行
            my_serial.Serial_Tx(0,0)
        if x1 is None and x2 is None:
            flag=1          
    

    if flag==1 :
        img_range1=result[50:240,70:200]
        x1,y1=ri_and_le.right_and_left(img_range1)
        if x1 is not None:
            #向左转
            dx=y1-y
            dy=x1-x

            angle_radians = math.atan(dy/dx)
            angle_degrees = math.degrees(angle_radians)
            print(angle_degrees)
            
            if angle_degrees>0:
                if angle_degrees>=30:
                    # 向左转              
                    my_serial.Serial_Tx(1,angle_degrees)

            if x1 is None:
                flag=2
        else:
            img_range2=result[50:240,440:570]
            x2,y2=ri_and_le.right_and_left(img_range2)
            if x2 is not None:
                dx=y2-y
                dy=x2-x

                angle_radians = math.atan(dy/dx)
                angle_degrees = math.degrees(angle_radians)
                print(angle_degrees)

                if angle_degrees<0:
                    angle_degrees=abs(angle_degrees)
                    if angle_degrees>=30:
                        #向右转
                        my_serial.Serial_Tx(2,angle_degrees)

                if x2 is None:                    
                    flag=3
    if flag==2:
        img_range2=result[50:240,440:570]
        x2,y2=ri_and_le.right_and_left(img_range2)
        if x2 is not None:
            #向右转
            dx=y2-y
            dy=x2-x

            angle_radians = math.atan(dy/dx)
            angle_degrees = math.degrees(angle_radians)
            print(angle_degrees)

            if angle_degrees<0:
                angle_degrees=abs(angle_degrees)
                if angle_degrees>=30:
                    #向右转
                    my_serial.Serial_Tx(2,angle_degrees)
        if x2 is None:
                flag=4
        
    if flag==3:
        img_range1=result[50:240,70:200]
        x1,y1=ri_and_le.right_and_left(img_range1)
        if x1 is not None:
            #向左转
            dx=y1-y
            dy=x1-x

            angle_radians = math.atan(dy/dx)
            angle_degrees = math.degrees(angle_radians)
            print(angle_degrees)
            
            if angle_degrees>0:
                if angle_degrees>=30:
                    # 向左转              
                    my_serial.Serial_Tx(1,angle_degrees)
            if x1 is None:
                flag=4

    if flag==4:
        #发送角度，应该是直行
        if x1 is not None or x2 is None:
            my_serial.Serial_Tx(0,0)

        if x1 is None or x2 is not None:
            my_serial.Serial_Tx(0,0)

        if x1 is None and x2 is None:
            flag=5

    if flag==5:
        img_range1=result[50:240,70:200]
        x1,y1=ri_and_le.right_and_left(img_range1)
        if x1 is not None :
            #直行
            my_serial.Serial_Tx(0,0)
        elif x1 is None and x2 is None:
            flag=6

        else :
            img_range2=result[50:240,440:570]
            x2,y2=ri_and_le.right_and_left(img_range2)
            if x2 is not None:
                #直行
                my_serial.Serial_Tx(0,0)
            if x1 is None and x2 is None:
                flag=7

    if flag==6:
        img_range1=result[50:240,70:200]
        x1,y1=ri_and_le.right_and_left(img_range1)
        if x1 is not None:
            #向左转
            dx=y1-y
            dy=x1-x

            angle_radians = math.atan(dy/dx)
            angle_degrees = math.degrees(angle_radians)
            print(angle_degrees)
            
            if angle_degrees>0:
                if angle_degrees>=30:
                    # 向左转              
                    my_serial.Serial_Tx(1,angle_degrees)
        if x1 is None:
            flag=8
        

    if flag==7:
        img_range2=result[50:240,440:570]
        x2,y2=ri_and_le.right_and_left(img_range2)
        if x2 is not None:
            #向右转
            #向右转
            dx=y2-y
            dy=x2-x

            angle_radians = math.atan(dy/dx)
            angle_degrees = math.degrees(angle_radians)
            print(angle_degrees)

            if angle_degrees<0:
                angle_degrees=abs(angle_degrees)
                if angle_degrees>=30:
                    #向右转
                    my_serial.Serial_Tx(2,angle_degrees)
        if x2 is None:
                    flag=8

    if flag==8:
        img_range1=result[50:240,70:200]
        img_range2=result[50:240,440:570]
        
        x1,y1=ri_and_le.right_and_left(img_range1)
        
        x2,y2=ri_and_le.right_and_left(img_range2)
        a=320
        b=240
        
        dx=y-b
        dy=x-a

        angle_radians = math.atan(dy/dx)
        angle_degrees = math.degrees(angle_radians)
        print(angle_degrees)

        angle_degrees=int(angle_degrees)
  
        if angle_degrees<0:
            if abs(angle_degrees)>=30:
                #该右转2
                my_serial.Serial_Tx(2,abs(angle_degrees))
        elif angle_degrees>0:
                #该左转1
            if angle_degrees>=30:
                my_serial.Serial_Tx(1,angle_degrees)
        elif abs(angle_degrees)<30:
                #直行
            my_serial.Serial_Tx(0,0) 
            
        if x1 is None and x2 is None:
            flag=9
            
            
    if flag==9:
    #直行
        my_serial.Serial_Tx(0,0)
                
     
           


def judge2(num_corners,result):
    contours,_=cv.findContours(result,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    if contours:
        contours=contours[0]
 
        leftmost=tuple(contours[contours[:,:,0].argmin()][0])
        rightmost=tuple(contours[contours[:,:,0].argmax()][0])
        print(f"最左点: {leftmost}")
        print(f"最右点: {rightmost}")
        cv.circle(result, leftmost, 10, (0, 255, 0), -1)  # 绿色表示最左点
        cv.circle(result, rightmost, 10, (0, 0, 255), -1)  # 红色表示最右点
        x1=leftmost[0]
        y1=leftmost[1]
        x2=rightmost[0]
        y2=rightmost[1]
        av_x=(x1+x2)//2
        av_y=(y1+y2)//2

        a=320
        b=240

        dx=av_x-a
        dy=av_y-b
        
        angle_radians = math.atan(dy/dx)
        angle_degrees = math.degrees(angle_radians)
        print(angle_degrees)

        angle_degrees=int(angle_degrees)

        if angle_degrees<0:
            if abs(angle_degrees)>=30:
                print("向右转")
                my_serial.Serial_Tx(2,abs(angle_degrees))
        elif angle_degrees>0:
            print("向左转")
            if angle_degrees>=30:
                my_serial.Serial_Tx(1,angle_degrees)
        return result

def judge4(num_corners,result):
    print(f"角点数量{num_corners}")
    under_img=result[240:,:]
    under_img,x1,y1,width,hight=up_and_down.under(under_img)
    result[240:,:]=under_img
    if x1 is None and y1 is None:
        x1=320
        y1=300
    
    a=320
    b=240
    
    cross(a,b,x1,y1)
    
    
    return result

