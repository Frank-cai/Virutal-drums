import pygame
import cv2 as cv
# import winsound
# import keyboard
import mediapipe as mp
import time


def wincam():
    # captures Webcam (may have to put another integer than 0 if you do not see through the wanted device)
    capture = cv.VideoCapture(0)

    # read sound file
    pygame.mixer.init()
    pygame.mixer.music.load("sound/drum_bass.mp3")

    # initialize a hand object
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    # used for fps
    previousTime = 0
    currentTime = 0

    while True:
        # capture Webcam frames
        isTrue, frame = capture.read()

        # process hands (currently maximum amount of hands is 2; if you want more or less hands see 'initialize a hand  object' mpHands.Hands())
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame = cv.flip(frame, 1)
        results = hands.process(frame)
        frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

        # generate landmarks on hands
        # print(results.multi_hand_landmarks)
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for index, lm in enumerate(handLms.landmark):
                    # print(index, lm)
                    h, w, c = frame.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)  # cx, cy -> center x and y (multiply float values(lm.x) with width/height of the image(in pixel))
                    # print(index, cx, cy)

                    if index == 10:  ## tip of thumb
                        cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                        print(index, cx, cy)
                        if cx >= w / 2:  ## right side of the screen
                            pygame.mixer.music.play()
                            # winsound.PlaySound('sound/snare.wav', winsound.SND_FILENAME)

                mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

        # display fps
        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime
        cv.putText(frame, str(int(fps)), (10, 80), cv.FONT_HERSHEY_TRIPLEX, 3, (0, 0, 0), 3)

        # display Webcam (until 'q' is pressed)
        cv.imshow('Webcam', frame)
        if cv.waitKey(20) & 0xFF == ord('q'):
            break

    # release and close everything
    capture.release()
    cv.destroyAllWindows()

"""
def camera():
    cap = cv.VideoCapture(0)

    drum_bass = vlc.MediaPlayer("sound/drum_bass.wav")
    drum_tom1 = vlc.MediaPlayer("sound/drum_tom1.wav")
    drum_tom2 = vlc.MediaPlayer("sound/drum_tom2.wav")
    drum_tom3 = vlc.MediaPlayer("sound/drum_tom3.wav")
    drum_snare = vlc.MediaPlayer("sound/drum_snare.wav")
    cymbal = vlc.MediaPlayer("sound/cymbal.wav")
    hi_hats = vlc.MediaPlayer("sound/hi_hats.wav")
    while True:
        ret, frame = cap.read()
        cv.imshow("capture", frame)
        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            drum_snare.stop()
            drum_snare.play()
        elif key == ord('w'):
            drum_bass.stop()
            drum_bass.play()
        elif key == ord('e'):
            cymbal.stop()
            cymbal.play()
        elif key == ord('p'):
            cap.release()
            cv.destroyAllWindows()
            return
"""

if __name__ == '__main__':
    wincam()
    # camera()
