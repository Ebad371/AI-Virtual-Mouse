import cv2
import mediapipe
import numpy
import autopy

cap = cv2.VideoCapture(0)
initHand = mediapipe.solutions.hands  

mainHand = initHand.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.8)
draw = mediapipe.solutions.drawing_utils  
wScr, hScr = autopy.screen.size()  #(1920 x 1080)
pX, pY = 0, 0  
cX, cY = 0, 0  


def handLandmarks(colorImg):
    landmarkList = []  

    landmarkPositions = mainHand.process(colorImg) 
    landmarkCheck = landmarkPositions.multi_hand_landmarks  
    if landmarkCheck:  
        for hand in landmarkCheck:  
            for index, landmark in enumerate(hand.landmark):  
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)  
                h, w, c = img.shape 
                centerX, centerY = int(landmark.x * w), int(landmark.y * h) 
                landmarkList.append([index, centerX, centerY])  
                
    return landmarkList


def fingers(landmarks):
    fingerTips = []  
    tipIds = [4, 8, 12, 16, 20]  
    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)
    
    # Check if fingers are up except the thumb
    for id in range(1, 5):
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:  # Checks to see if the tip of the finger is higher than the joint
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips


while True:
    check, img = cap.read()  
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
    lmList = handLandmarks(imgRGB)
    
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  
        x2, y2 = lmList[12][1:] 
        finger = fingers(lmList)  
        print(finger)
        if finger[1] == 1 and finger[0] == 0:  # Checks to see if the pointing finger is up and thumb finger is down
            x3 = numpy.interp(x1, (75, 640 - 75), (0, wScr))  # Converts the width of the window relative to the screen width
            y3 = numpy.interp(y1, (75, 480 - 75), (0, hScr))  # Converts the height of the window relative to the screen height
            
            cX = pX + (x3 - pX) / 7  
            cY = pY + (y3 - pY) / 7  
            
            autopy.mouse.move(wScr-cX, cY)  # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            pX, pY = cX, cY 

        if finger[1] == 1 and finger[2] == 1:  # Checks to see if the pointer finger is down and thumb finger is up
            autopy.mouse.click()  # Left click
        
            
    cv2.imshow("AI Virtual Mouse", img)
    if cv2.waitKey(1) & 0xFF == ord('c'):
        break
