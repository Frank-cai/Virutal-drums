import cv2 as cv
import winsound
# import keyboard
import mediapipe as mp
import time

## captures Webcam (may have to put another integer than 0 if you do not see through the wanted device)
capture = cv.VideoCapture(0, cv.CAP_DSHOW)

## initialize a hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

## used for fps
previousTime = 0
currentTime = 0

while True:
    ## play sound by pressing s
    # if keyboard.is_pressed('s'):
    #     winsound.PlaySound('sound/snare.wav', winsound.SND_FILENAME)

    ## capture Webcam frames
    isTrue, frame = capture.read()

    ## process hands (currently maximum amount of hands is 2; if you want more or less hands see 'initialize a hand object' mpHands.Hands())
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    ## generate landmarks on hands
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for index, lm in enumerate(handLms.landmark):
                # print(index, lm)
                h, w, c = frame.shape
                cx, cy = int(lm.x*w), int(lm.y*h)  ## cx, cy -> center x and y (multiply float values(lm.x) with width/height of the image(in pixel))
                # print(index, cx, cy)

                if index == 4:  ## tip of thumb
                    cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                    print(index, cx, cy)
                    if cx >= w/2:  ## right side of the screen
                        winsound.PlaySound('sound/snare.wav', winsound.SND_FILENAME)

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    ## display fps
    currentTime = time.time()
    fps = 1/(currentTime-previousTime)
    previousTime = currentTime
    cv.putText(frame, str(int(fps)), (10, 80), cv.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 3)

    ## display Webcam (until 'q' is pressed)
    cv.imshow('Webcam', frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

## release and close everything
capture.release()
cv.destroyAllWindows()
