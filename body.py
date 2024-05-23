import cv2
import mediapipe as mp
import math

video = cv2.VideoCapture(0)
# video = cv2.VideoCapture('./Burpee.mp4')
# video = cv2.VideoCapture('./Burpee.mp4')
pose = mp.solutions.pose
Pose = pose.Pose(min_tracking_confidence=0.5,min_detection_confidence=0.5)
draw = mp.solutions.drawing_utils
contadorPolichinelo = 0
contadoBurp = 0
contadorFlexao = 0
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

def flexao(ic_flexao, distOmbroMao, distMOPE, contadorFlexao):
       if ic_flexao == True and distOmbroMao <= 208 and distMOPE <=116 and distMOPE > 110:
           contadorFlexao +=1
           ic_flexao = False
           print(distMOPE)

       if distOmbroMao > 300:
           ic_flexao = True

       return ic_flexao, contadorFlexao

def countDist():
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

        return distMO, distPE, distMOPE, distOmbroMao



def exibirCounter(contadorFlexao, contadorPolichinelo, contadoBurp):
    # Definir tamanho fixo e pequeno para a fonte e a caixa
    font_scale = 0.5
    font_thickness = 1
    box_thickness = 1  # Alterando a espessura da borda da caixa
    blue_color = (255, 0, 0)  # Definindo a cor azul
    margin = 10  # Margem dos cantos

    if contadorFlexao >= 1:
        textoFlexao = f'Flexões: {contadorFlexao}'
        # Determinar a altura do texto
        (text_width, text_height), _ = cv2.getTextSize(textoFlexao, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        box_height = text_height + 20  # Definir a altura da caixa com uma pequena margem

        # Determinar as coordenadas para a caixa
        x1, y1 = margin, margin
        x2, y2 = 200 + margin, box_height + margin
        # Desenhar fundo azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, cv2.FILLED)
        # Desenhar borda azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, box_thickness)
        cv2.putText(frame, textoFlexao, (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    if contadorPolichinelo >= 1:
        textoPolichinelo = f'Polichinelos: {contadorPolichinelo}'
        # Determinar a altura do texto
        (text_width, text_height), _ = cv2.getTextSize(textoPolichinelo, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        box_height = text_height + 20  # Definir a altura da caixa com uma pequena margem

        # Determinar as coordenadas para a caixa
        x1, y1 = margin, 200 + margin
        x2, y2 = 200 + margin,  box_height + 200 + margin
        # Desenhar fundo azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, cv2.FILLED)
        # Desenhar borda azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, box_thickness)
        cv2.putText(frame, textoPolichinelo, (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    if contadoBurp >= 1:
        textoBurp = f'Burpees: {contadoBurp}'
        # Determinar a altura do texto
        (text_width, text_height), _ = cv2.getTextSize(textoBurp, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
        box_height = text_height + 20  # Definir a altura da caixa com uma pequena margem

        # Determinar as coordenadas para a caixa
        x1, y1 = margin, 390 + margin
        x2, y2 = 200 + margin, box_height + 390 + margin
        # Desenhar fundo azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, cv2.FILLED)
        # Desenhar borda azul
        cv2.rectangle(frame, (x1, y1), (x2, y2), blue_color, box_thickness)
        cv2.putText(frame, textoBurp, (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)






while True:
    success,frame = video.read()
    videoRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = Pose.process(videoRGB)
    points = results.pose_landmarks
    draw.draw_landmarks(frame,points,pose.POSE_CONNECTIONS)
    points = results.pose_landmarks
    draw.draw_landmarks(frame,points,pose.POSE_CONNECTIONS)
    h,w,_ = frame.shape
        
    if points:
        distMO, distPE, distMOPE, distOmbroMao = countDist()
        
        ic_polichinelo, contadorPolichinelo = polichinelo(ic_polichinelo, contadorPolichinelo, distMO, distPE)

        ic_burp, contadoBurp, ic_flexao = burp(ic_burp, contadoBurp, distMOPE, distPE, ic_flexao)

        ic_flexao, contadorFlexao = flexao(ic_flexao, distOmbroMao, distMOPE, contadorFlexao )

        exibirCounter(contadorFlexao, contadorPolichinelo, contadoBurp )


        frame = cv2.resize(frame, (1280, 720))

        
    cv2.imshow('Result', frame)
    cv2.waitKey(1)




