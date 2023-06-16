import cv2
import numpy as np
import time
import PoseModule as pm
import datetime
import requests
from GenerateReport import GeneratePdfReport

# get current date

cap = cv2.VideoCapture(0)

detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0


def updatedata(c):
    url="https://ptrainer-567d7-default-rtdb.firebaseio.com/pt.json"
    new_data={str(datetime.date.today()):c}
    post_response = requests.patch(url, json=new_data)


while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("AiTrainer/test.jpg")
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    prev=0
    if len(lmList) != 0:
        # Right Arm
        angle = detector.findAngle(img, 12, 14, 16)
        # # Left Arm
        # angle = detector.findAngle(img, 11, 13, 15,False)
        per = np.interp(angle, (210, 305), (0, 100))
        bar = np.interp(angle, (220, 305), (650, 100))
        if(angle<190):
            per = np.interp(angle, (70, 160), (100, 0))
            bar = np.interp(angle, (70, 160), (100, 650))
        print( per,bar)
        # Check for the dumbbell curls
        color = (0, 0, 255)
        if per == 100:
            color = (0, 255, 0)
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            color = (0, 255, 0)
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)


        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4)
        # if prev!=int(count):
        #     updatedata(int(count))
        #     prev=int(count)
        # Draw Curl Count
        # cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED) 1
        cv2.putText(img, "Reps "+str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 5,
                    (50, 0, 225), 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "fps "+str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 2,
                (0, 0, 225), 5)

    cv2.imshow("Image", img)
    keyCode=cv2.waitKey(1)
    if (keyCode & 0xFF) == ord("q"):
        updatedata(int(count))
        cv2.destroyAllWindows()
        GeneratePdfReport()
        break
