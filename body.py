import cv2
import mediapipe as mp
import math


video = cv2.VideoCapture('./Polichinelo.mp4')
#video = cv2.VideoCapture('./Burpee.mp4')
#ideo = cv2.VideoCapture('./Flexao.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
contadorPolichinelo = 0
contadoBurp = 0
contadoFlexao = 0
check = False
ic_polichinelo = False
ic_burp = False
ic_flexao = False



def polichinelo (ic_polichinelo, contadorPolichinelo, distMO, distPE):
        if ic_polichinelo == True and distMO <=90 and distPE >=200:
            contadorPolichinelo +=1
            ic_polichinelo = False

        if distMO >150 and distPE <150:
           ic_polichinelo = True

        return ic_polichinelo, contadorPolichinelo

def burp ( ic_burp, contadoBurp, distMOPE, distPE, ic_flexao):
        if ic_burp == True and distMOPE >=1450 and distPE < 100:
            contadoBurp +=1
            ic_burp = False   
            ic_flexao = False
            

        if distMOPE < 150:
           ic_burp = True


        return ic_burp, contadoBurp, ic_flexao

def flexao(ic_flexao, distOmbroMao, distMOPE, contadoFlexao):
       if ic_flexao == True and distOmbroMao <= 208 and distMOPE <=116 and distMOPE > 110:
           contadoFlexao +=1
           ic_flexao = False
           print(distMOPE)

       if distOmbroMao > 300:
           ic_flexao = True

       return ic_flexao, contadoFlexao

while True:
    success,img = video.read()
    videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)
    points = results.pose_landmarks
    draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)
    h,w,_ = img.shape
        


    if points:
        peDY = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].y*h)
        peDX = int(points.landmark[pose.PoseLandmark.RIGHT_FOOT_INDEX].x*w)

        peEY = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].y*h)
        peEX = int(points.landmark[pose.PoseLandmark.LEFT_FOOT_INDEX].x*w)

        moDY = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].y*h)
        moDX = int(points.landmark[pose.PoseLandmark.RIGHT_INDEX].x*w)

        moEY = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].y*h)
        moEX = int(points.landmark[pose.PoseLandmark.LEFT_INDEX].x*w)

        omDY = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].y*h)
        omDX = int(points.landmark[pose.PoseLandmark.RIGHT_SHOULDER].x*w)

        distMO = math.hypot(moDX-moEX,moDY-moEY)
        distPE = math.hypot(peDX-peEX,peDY-peEY)

        distMOPE = math.hypot((peDX-moDX) - (peEX-moEX),(moDY-peEY) - (peDY-moEY) )

        distOmbroMao = math.hypot((omDY - omDX) - ((moDX-moDY) - 110 ))

        
        
        ic_polichinelo, contadorPolichinelo = polichinelo(ic_polichinelo, contadorPolichinelo, distMO, distPE)

        ic_burp, contadoBurp,ic_flexao = burp(ic_burp, contadoBurp, distMOPE, distPE, ic_flexao)

        ic_flexao, contadoFlexao = flexao(ic_flexao, distOmbroMao, distMOPE, contadoFlexao )
        
        
        
        if (contadoFlexao >= 1):
                textoFlexao = f'QTD flexão {contadoFlexao}'
                cv2.rectangle(img,(20,240),(650,120),(255,0,0),-1)
                cv2.putText(img,textoFlexao,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        if (contadorPolichinelo >= 1):
                textoPolichinelo = f'QTD Polichinelo {contadorPolichinelo}'
                cv2.rectangle(img,(20,240),(650,120),(255,0,0),-1)
                cv2.putText(img,textoPolichinelo,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        if (contadoBurp >= 1):
                textoBurp = f'QTD Burp {contadoBurp}'
                cv2.rectangle(img,(20,240),(650,120),(255,0,0),-1)
                cv2.putText(img,textoBurp,(40,370),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        
    cv2.imshow('Result', img)
    cv2.waitKey(1)




