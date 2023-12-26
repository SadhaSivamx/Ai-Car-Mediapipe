import cv2
import mediapipe
from time import  sleep
ctime = 0
ptime = 0
ele=0
import serial
import time
tx=""
Data=""
# Establish serial connection (change 'COM8' to your Arduino's port)
ser = serial.Serial('COM4', 115200)
# Delay to allow Arduino to reset after establishing serial connection
time.sleep(2)
cap = cv2.VideoCapture(0)

medhands = mediapipe.solutions.hands
hands = medhands.Hands(max_num_hands=1, min_detection_confidence=0.7)
draw = mediapipe.solutions.drawing_utils
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    res = hands.process(imgrgb)

    lmlist = []
    tipids = [4, 8, 12, 16, 20]  # list of all landmarks of the tips of fingers

    cv2.rectangle(img, (20, 350), (150, 440), (0, 255, 204), cv2.FILLED)
    cv2.rectangle(img, (20, 350), (150, 440), (0, 0, 0), 5)

    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):

                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if len(lmlist) != 0 and len(lmlist) == 21:
                    fingerlist = []

                    # thumb and dealing with flipping of hands
                    if lmlist[12][1] > lmlist[20][1]:
                        if lmlist[tipids[0]][1] > lmlist[tipids[0] - 1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    else:
                        if lmlist[tipids[0]][1] < lmlist[tipids[0] - 1][1]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)

                    # others
                    for id in range(1, 5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:
                            fingerlist.append(1)
                        else:
                            fingerlist.append(0)
                    fingers=fingerlist.count(1)
                    if fingers!=ele:
                        ele=fingers
                        print(ele)
                        if ele==0:
                            Data="0"
                            tx="STOPPING"
                        if ele==5:
                            Data="1"
                            tx = "FORWARD"
                        if ele==1:
                            Data="2"
                            tx = "BACKWARD"
                        if ele==2:
                            Data="3"
                            tx = "LEFTWARD"
                        if ele==3:
                            Data="4"
                            tx = "RIGHTWARD"
                        ser.write(Data.encode('utf-8'))
                        sleep(0.2)
                    pos=(40, 405)
                    color = (0, 0, 0)
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(img,tx , pos, font,0.6,color, 2)

                # change color of points and lines
                draw.draw_landmarks(img, handlms, medhands.HAND_CONNECTIONS,
                draw.DrawingSpec(color=(0, 255, 204), thickness=2, circle_radius=2),
                draw.DrawingSpec(color=(0, 0, 0), thickness=2, circle_radius=3))

    # fps counter
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    # fps display
    cv2.putText(img, f'FPS:{str(int(fps))}', (0, 12), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1)

    cv2.imshow("LED-Control", img)

    # press q to quit
    if cv2.waitKey(1) == ord('q'):
        break
ser.close()
cv2.destroyAllWindows()
