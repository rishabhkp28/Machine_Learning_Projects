import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands#solution submodule has various methods to determine body landmarks we chose hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,1,
                                        self.detectionCon, self.trackCon)#created the hand object
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]#my finger tips

    def findHands(self, img, draw=True):# draws connectors on joints
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)#color format from bgr to rgb
        self.results = self.hands.process(imgRGB) #process the image for hands
        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks: #whether i got some landmarks or not (maybe multiple hands)
            for handLms in self.results.multi_hand_landmarks: #traversing those landmarks(traversing every hand)
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    #draw drawing_utillity of mp solution's submodule draws connections and here those are hand_connections(frozenset)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        '''basically draws bounding boxes on hands just on my hand
        also  points the joints and then also stores the position of joints no my hand within the frame'''
        xList = []
        yList = []
        bbox = []
        self.lmList = [] #its now public , landmark list
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(
                    myHand.landmark): #myhand.landmark has the location of landmarks of my hand
                # print(id, lm) eg
                '''myHand.landmark = [
                               its list {'x': 0.5, 'y': 0.6, 'z': 0.0},  # id 0: Wrist
                                        {'x': 0.45, 'y': 0.55, 'z': 0.0}, # id 1: Thumb CMC
                                        {'x': 0.4, 'y': 0.5, 'z': 0.0},   # id 2: Thumb MCP
                                        {'x': 0.35, 'y': 0.45, 'z': 0.0}, # id 3: Thumb PIP
                                        {'x': 0.3, 'y': 0.4, 'z': 0.0},   # id 4: Thumb Tip
                                        # ... other landmarks
                                    ]
                '''
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                xList.append(cx)
                yList.append(cy)
                print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)# circles the joints

            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax

            if draw:
                cv2.rectangle(img, (xmin - 35, ymin - 35), (xmax + 35, ymax + 35),
                              (0, 255, 0), 2)


        return self.lmList, bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
            '''checking the x axis for thumb it must be to left than its lower joint if its up
            rest all fingers must be above the below joint landmark if they are up
            '''
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):

            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # totalFingers = fingers.count(1)

        return fingers #compare it against the tipsId list definded inside the constructor



    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        print("p1 is",p1)
        x1,y1,x2,y2,cx,cy=0,0,0,0,0,0
        if len(self.lmList) >= max(p1, p2) + 1:
        #landmark list contains the landmarks of my hand which i got from previous along with their location
            x1, y1 = self.lmList[p1][1:]
            x2, y2 = self.lmList[p2][1:] #extract x and y coordinated of landmark with ids p1 and p2
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1) # calculates the eucledian distance

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), 2, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(length), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 0, 0), 1 )#size an thickness respectively
        return length, img, [x1, y1, x2, y2, cx, cy]
def main():
    cap = cv2.VideoCapture(0)  # Start capturing video from the webcam
    detector = handDetector()  # Create an instance of the handDetector class
    pTime = 0  # Initialize pTime here
    while True:
        success, img = cap.read()  # Read a frame from the video capture
        img = cv2.flip(img, 1)  # Flip the image horizontally
        if not success:
            break
        img = detector.findHands(img)  # Use the findHands method to process the image and draw hand landmarks
        lmList, bbox = detector.findPosition(img)

        detector.findDistance(4,8,img)
        if len(lmList) != 0:
            print(lmList[4])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str("Frame Rate : "+str(int(fps))), (10, 70), cv2.FONT_HERSHEY_PLAIN, 1,
                    (255, 0, 255), 1)
        cv2.imshow("Image", img)  # Display the processed image
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Break the loop if 'q' is pressed
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()