import cv2
import mediapipe as mp
from robodk.robolink import *
from robodk.robomath import *

RDK = Robolink()
RDK.ShowRoboDK()
robot = RDK.Item('', ITEM_TYPE_ROBOT)
robot.setJoints([0,0,0,0,0,0])
pose = robot.Pose()
xyz = pose_2_xyzrpw(pose)

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 30)
mpHands = mp.solutions.hands
hands = mpHands.Hands(0.75)
mpDraw = mp.solutions.drawing_utils
mp_drawingStyles = mp.solutions.drawing_styles

pTime = 0
arr1 = []
arr2 = []
kx = 0
ky = 0
kz = 0
tempx = 0
tempy = 0
tempz = 0
tempzx = 0
tempzy = 0

while True:
    if len(arr1) >= 2 and len(arr2)>=2:
        try:
            tempzx = abs(arr1[5]-arr1[17])
            tempzy = abs(arr2[5]-arr2[17])
            tempz = sqrt(pow(tempzx,2) + pow(tempzy,2))

            for i in range(len(arr1)):
                tempx += arr1[i]

            for i in range(len(arr2)):
                tempy += arr2[i]

            tempx = tempx /21
            tempy = tempy/21

            if ky < tempx and abs(kx-tempx)>=5 :
                print("left")
                xyz[1] = xyz[1] + 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)
            if ky > tempx and abs(kx-tempx) >= 5 :
                print("right")
                xyz[1] = xyz[1] - 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)

            if kx < tempy and abs(ky-tempy) >=3 :
                print("down")
                xyz[2] = xyz[2] - 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)
            if kx > tempy and abs(ky-tempy) >3:
                print("up")
                xyz[2] = xyz[2] + 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)

            if kz < tempz and abs(kz-tempz)>3 :
                print("forward")
                xyz[0] = xyz[0] + 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)

            if kz > tempz and abs(kz-tempz)>2 :
                print("backward")
                xyz[0] = xyz[0] - 20
                pose = xyzrpw_2_pose(xyz)
                robot.MoveJ(pose)

            if abs(kx-tempx)>5 and abs(ky-tempy)>3 :
                print("stable")

            kx = tempx
            ky = tempy
            kz = tempz
            arr2.clear()
            arr1.clear()
        except:
            xyz[0] = xyz[0] - 30
            xyz[1] = xyz[1] - 30
            xyz[2] = xyz[2] - 30
        
    success, img = cam.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    resultsHD = hands.process(imgRGB)

    ct = time.time()
    if resultsHD.multi_hand_landmarks:
        myHand = resultsHD.multi_hand_landmarks[0]
        for id, lm in enumerate(myHand.landmark):
                for handLm in resultsHD.multi_hand_landmarks:
                    mpDraw.draw_landmarks(img, handLm, mpHands.HAND_CONNECTIONS)
                h, w, _ = img.shape

                cx = int(lm.x * w)
                cy = int(lm.y * h)
                arr1.append(cx)
                arr2.append(cy)


    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break