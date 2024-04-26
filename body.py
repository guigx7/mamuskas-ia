


import cv2
import mediapipe as mp
import math


video = cv2.VideoCapture('./Polichinelo.mp4')
#video = cv2.VideoCapture('./Burpee.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
contadorPolichinelo = 0
contadoBurp = 0
check = True

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

        distMO = math.hypot(moDX-moEX,moDY-moEY)
        distPE = math.hypot(peDX-peEX,peDY-peEY)

        distMOPE = math.hypot((peDX-moDX) - (peEX-moEX),(moDY-peEY) - (peDY-moEY) )


        print(f'maos {distMO} pes {distPE}')
        print(f'DISTANCIA MAO E PE {distMOPE}')

        # maos <=150 pes >=150 

        #VIDEO MP4 distMO <=90 and distPE >=200

        if check == True and distMO <=90 and distPE >=200:
            contadorPolichinelo +=1
            check = False
#
        if distMO >150 and distPE <150:
           check = True


        if check == True and distMOPE >=1450 and distPE < 100:
            contadoBurp +=1
            check = False   

        
        if distMOPE < 150:
           check = True


        textoPolichinelo = f'QTD {contadorPolichinelo}'
        cv2.rectangle(img,(20,240),(450,120),(255,0,0),-1)
        cv2.putText(img,textoPolichinelo,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

        textoBurp = f'QTD Burp {contadoBurp}'
        cv2.rectangle(img,(20,300),(350,420),(255,0,0),-1)
        cv2.putText(img,textoBurp,(40,200),cv2.FONT_HERSHEY_SIMPLEX,2,(255,255,255),5)

    cv2.imshow('Result', img)
    cv2.waitKey(1)




