import cv2
from matplotlib import pyplot as plt
import numpy as np
import mediapipe as mp


video = cv2.VideoCapture('./polichinelo.gif')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils


while True:
    success,img = video.read()
    videoRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    draw.draw_landmarks(img,points,pose.POSE_CONNECTIONS)

    cv2.imshow('Result', img)
    cv2.waitKey(10)




