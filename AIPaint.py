from enum import Flag
from sre_constants import SUCCESS
from matplotlib.pyplot import draw
import numpy as np
import cv2
import os


from requests import head
import HandTrackingModule as htm


brushThickness=15
eraserThickness=80

#ColorPicker(Header)
folderPath="Header"
myList=os.listdir(folderPath)


overlayList=[]
for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

header=overlayList[0]
drawColor=(0,255,0)#defaultcolor=green

cap=cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

frame_width=int(cap.get(3))
frame_height=int(cap.get(4))
size=(frame_width,frame_height)
result=cv2.VideoWriter('output.mp4',cv2.VideoWriter_fourcc(*'XVID'),30,size)

xp=0
yp=0

imgCanvas=np.zeros((720,1280,3),np.uint8)


detector=htm.handDetector(detectionCon=0.85)

while True:
    ret,img=cap.read()
    img=cv2.flip(img,1)

    #find the hand landmarks
    img=detector.findHands(img)
    lmList=detector.findPosition(img,draw=False)

    if len(lmList)!=0:
        #print(lmList)
        x1,y1=lmList[8][1:] #index finger
        x2,y2=lmList[12][1:] #middle finger

        #check the finger
        fingers=detector.fingersUp()
        #print(fingers)


    #if two fingers are up 
        if fingers[1] and fingers[2]:
            xp,yp=0,0
            
            #if we are in header (color picker)

            if y1<125:
                if 150<x1<350:
                    header=overlayList[0]
                    drawColor=(0,255,0)
                    
                elif 450<x1<650:
                    header=overlayList[1]
                    drawColor=(0,0,255)
                  
                elif 750<x1<950:
                    header=overlayList[2] 
                    drawColor=(255,0,0)
               
                elif 1000<x1<1250:
                    header=overlayList[3]  
                    
                    #eraser
                    drawColor=(0,0,0)


            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)           

        #if Drawing mode(when one finger is up) 
        if fingers[1] and fingers[2]==False:
            

            if xp==0 and yp==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)
            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)


    #set the header image    
    img[0:125,0:1280]=header

    result.write(img) 

    cv2.imshow("Image",img)
    #cv2.imshow("Canvas",imgCanvas)
    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break 
cap.release()
cv2.destroyAllWindows()