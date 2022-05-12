from unittest import result
import cv2
import mediapipe as mp



class handDetector():
    def __init__(self,mode=False,maxHands=2,modelComplexity=1,detectionCon=0.5,trackCon=0.5):

        self.mode=mode
        self.maxHands=maxHands
        self.modelComplex = modelComplexity
        self.detectionCon=detectionCon
        self.trackCon=trackCon

        self.mpHands=mp.solutions.hands
        self.hands=self.mpHands.Hands(self.mode,self.maxHands,self.modelComplex,
        self.detectionCon,self.trackCon)
        self.mpDraw=mp.solutions.drawing_utils  
        self.tipIds=[4,8,12,16,20] 

    def  findHands(self,img,draw=True):
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            #get the information of each hand
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
        self.lmList=[]
        if self.results.multi_hand_landmarks:
            myHand=self.results.multi_hand_landmarks[handNo]
            for id,lm in enumerate(myHand.landmark):
              
                h,w,c=img.shape
                cx,cy=int(lm.x*w),int(lm.y*h)
             
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),8,(255,0,0),cv2.FILLED)
        return self.lmList    

    def fingersUp(self):
        fingers=[]

        if self.lmList[self.tipIds[0]][1]<self.lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1,5):
                if self.lmList[self.tipIds[id]][2]<self.lmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0) 
        return fingers               


mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils


def main():
  
    cap=cv2.VideoCapture(0)
    detector=handDetector()

    while True:
        success,img=cap.read()
        img=detector.findHands(img)
        lmsList=detector.findPosition(img)
      

        cv2.imshow("Image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=="__main__":
    main()    