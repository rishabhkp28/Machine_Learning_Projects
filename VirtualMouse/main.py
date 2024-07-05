import cv2
import numpy as np
import HandTrackingModule as htm
import pyautogui
import time

wCam,hCam = 640,480;
frameR = 50
smoothening = 1
cap = cv2.VideoCapture(0)#no of cameras
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector(maxHands=1)
screen_width, screen_height = pyautogui.size()

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

while(True):
       # 1. Find hand Landmarks
       success, img = cap.read()  # Capture the next frame from the camera
       if not success:
           print("Failed to capture frame")
           break
       cv2.imshow("Image", img)      # Display the captured frame in a window named "Image"
       img = cv2.flip(img, 1)  # Flip around the vertical axis (horizontal flip)
       img = detector.findHands(img) #detector.findHands(img) processes the image to detect hands and draw landmarks on the hands.
       '''detector.findPosition(img) extracts the positions of the hand landmarks from the processed image.
          lmList is a list of landmark positions. Each landmark is represented by an (x, y) coordinate.
           bbox is a bounding box around the detected hand.'''
       lmList, bbox = detector.findPosition(img)
       # 2. Get the tip of the index and middle fingers
       if (len(lmList) != 0): #checks if the landmarks were detected
           x1, y1 = lmList[8][1:] #(index finger co.)it is a list of lists from where we extracted x ,y coordinates only by slicing
           x2, y2 = lmList[12][1:]# middle finger coordinates
           #x1,y1 gets impression of thumn and the x2 and y2 helps me get the indexx finger
           # 3. Check which fingers are up
           fingers = detector.fingersUp()
           # print(fingers)
           cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),(255, 0, 255), 2)

           #New functionality (to scroll up or down) for up we use three fingers and for down we use 4 fingers
           #up
           if fingers[1]==1 and fingers[2]==1 and fingers[3]==1 and fingers[4]==0:
               pyautogui.scroll(40)  # Scroll up
               cv2.putText(img, "Scroll Up", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

            #down
           if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[4] == 1:
               pyautogui.scroll(-40)  # Scroll down
               cv2.putText(img, "Scroll Down", (10, 100), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

           #4 Mouse cursor moving using index finger
           if fingers[1] == 1 and fingers[2] == 0:
               # 5. Convert Coordinates
               x3 = np.interp(x1, (frameR, wCam - frameR), (0, screen_width))
               y3 = np.interp(y1, (frameR, hCam - frameR), (0, screen_height))
               '''
               Both above lines define the total area where we can interpolate the webcam finger pointer 
               frameR prevents edging effects           
               '''
               # 6. Smoothen Values
               '''adjusting mouse senstivity'''
               clocX = plocX + (x3 - plocX) / smoothening
               clocY = plocY + (y3 - plocY) / smoothening
               # 7. Move Mouse
               pyautogui.moveTo(clocX, clocY)
               cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
               plocX, plocY = clocX, clocY
               # 8. Both Index and middle fingers are up : Clicking Mode
           length=0
           lineInfo = []
           if fingers[1] == 1 and fingers[2] == 1 and fingers[3] ==0 and fingers[4]==0:
               # 9. Find distance between fingers
               length, img, lineInfo = detector.findDistance(8, 12, img) # we got the distance , and an image and coordinated of diff points on line
               print(length)
               # 10. Click mouse if distance short
               if length < 30:
                    cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
       # 11. Frame Rate
       cTime = time.time()
       fps = 1 / (cTime - pTime)
       pTime = cTime
       cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                       (255, 0, 0), 3)
       # 12. Display
       cv2.imshow("Image", img)
       # Exit if 'q' is pressed
       if cv2.waitKey(1) & 0xFF == ord('q'):
           break
