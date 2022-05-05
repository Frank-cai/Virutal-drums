import cv2 as cv
import mediapipe as mp
import time
import cvzone
import numpy as np
from functions import image_resize
from functions import gesture
import pygame

## variables
sound_snare_path = "sound/drum_snare.mp3"
sound_tom_path   = "sound/drum_tom1.mp3"
sound_bass_path  = "sound/drum_bass.mp3"
sound_crash_path = "sound/cymbal.mp3"
sound_ride_path  = "sound/hihat.mp3"

image_snare_path = "images/snare.png"
image_tom_path   = "images/tom.png"
image_bass_path  = "images/bass.png"
image_crash_path = "images/crash.png"
image_ride_path  = "images/ride.png"

border_offset = 10

## used for fps
previousTime = 0
currentTime = 0

## captures Webcam (may have to put another integer than 0 if you do not see through the wanted device)
capture = cv.VideoCapture(0, cv.CAP_DSHOW)

## used for images (scaling/positioning)
isTrue, frame = capture.read()
frame_h, frame_w, frame_c = frame.shape
picture_height = frame_h * 0.25

## read sound files
pygame.mixer.init()
snare_sound = pygame.mixer.Sound(sound_snare_path)
tom_sound = pygame.mixer.Sound(sound_tom_path)
bass_sound = pygame.mixer.Sound(sound_bass_path)
crash_sound = pygame.mixer.Sound(sound_crash_path)
ride_sound = pygame.mixer.Sound(sound_ride_path)

## initialize a hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
position = 0
joint_list = [[5, 6, 7], [9, 10, 11], [13, 14, 15], [17, 18, 19]]

## snare image
snare_img = cv.imread(image_snare_path, cv.IMREAD_UNCHANGED)
snare_img = image_resize(snare_img, height=int(picture_height))
snare_img_h, snare_img_w, snare_img_c = snare_img.shape
## tom image
tom_img = cv.imread(image_tom_path, cv.IMREAD_UNCHANGED)
tom_img = image_resize(tom_img, height=int(picture_height))
tom_img_h, tom_img_w, tom_img_c = tom_img.shape
## bass image
bass_img = cv.imread(image_bass_path, cv.IMREAD_UNCHANGED)
bass_img = image_resize(bass_img, height=int(picture_height))
bass_img_h, bass_img_w, bass_img_c = bass_img.shape
## crash image
crash_img = cv.imread(image_crash_path, cv.IMREAD_UNCHANGED)
crash_img = image_resize(crash_img, height=int(picture_height))
crash_img_h, crash_img_w, crash_img_c = crash_img.shape
## ride image
ride_img = cv.imread(image_ride_path, cv.IMREAD_UNCHANGED)
ride_img = image_resize(ride_img, height=int(picture_height))
ride_img_h, ride_img_w, ride_img_c = ride_img.shape

while True:
    ## capture Webcam frames
    isTrue, frame = capture.read()

    ## process hands (currently maximum amount of hands is 2; if you want more or less hands see 'initialize a hand object' mpHands.Hands())
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    ## generate landmarks on hands
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            """
            for index, lm in enumerate(handLms.landmark):
                # print(index, lm)
                cx, cy = int(lm.x*frame_w), int(lm.y*frame_h)  ## cx, cy -> center x and y (multiply float values(lm.x) with width/height of the image(in pixel))
                # print(index, cx, cy)

                if index == 12:  ## tip of middle finger
                    cv.circle(frame, (cx, cy), 10, (255, 0, 255), cv.FILLED)
                    #print(index, cx, cy)
                    if border_offset <= cx <= snare_img_w + border_offset and frame_h - snare_img_h - border_offset <= cy <= frame_h - border_offset:  ## right side of the screen
                        snare_sound.play()
                    elif frame_w - tom_img_w - border_offset <= cx <= frame_w - border_offset and frame_h - tom_img_h - border_offset <= cy <= frame_h - border_offset:
                        tom_sound.play()
                    elif int((frame_w - bass_img_w)/2) <= cx <= int((frame_w - bass_img_w)/2) + bass_img_w and frame_h - bass_img_h - border_offset <= cy <= frame_h - border_offset:
                        bass_sound.play()
                    elif border_offset <= cx <= border_offset + crash_img_w and border_offset <= cy <= border_offset + crash_img_h:
                        crash_sound.play()
                    elif frame_w - ride_img_w - border_offset <= cx <= frame_w - border_offset and border_offset <= cy <= ride_img_h:
                        ride_sound.play()
            """
            flag = gesture(handLms, joint_list)
            if flag:
                if handLms.landmark[8].y*frame_h < border_offset+ride_img_h and handLms.landmark[8].x*frame_w > frame_w - ride_img_w - border_offset:
                    if position != 1:
                        ride_sound.play()
                    position = 1
                elif handLms.landmark[8].y*frame_h < border_offset+crash_img_h and handLms.landmark[8].x*frame_w < border_offset+crash_img_w:
                    if position != 2:
                        crash_sound.play()
                    position = 2
                elif handLms.landmark[8].y*frame_h > frame_h - snare_img_h - border_offset \
                        and handLms.landmark[8].x*frame_w < 0 + border_offset + snare_img_w:
                    if position != 3:
                        snare_sound.play()
                    position = 3
                elif handLms.landmark[8].y*frame_h > frame_h - bass_img_h - border_offset \
                        and int((frame_w + bass_img_w) / 2) > handLms.landmark[8].x*frame_w > int((frame_w - bass_img_w) / 2):
                    if position != 4:
                        bass_sound.play()
                    position = 4
                elif handLms.landmark[8].y*frame_h > frame_h - tom_img_h - border_offset \
                        and handLms.landmark[8].x*frame_w > frame_w - tom_img_w - border_offset:
                    if position != 5:
                        tom_sound.play()
                    position = 5
                else:
                    position = 0

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    ## add fps to webcam
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv.putText(frame, str(int(fps)), (int(frame_w / 2 - frame_w / 10), 80), cv.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 0), 3)

    ## add drum parts to webcam
    frame = cvzone.overlayPNG(frame, snare_img, [0 + border_offset, frame_h - snare_img_h - border_offset])
    frame = cvzone.overlayPNG(frame, tom_img,
                              [frame_w - tom_img_w - border_offset, frame_h - tom_img_h - border_offset])
    frame = cvzone.overlayPNG(frame, bass_img, [int((frame_w - bass_img_w) / 2), frame_h - bass_img_h - border_offset])
    frame = cvzone.overlayPNG(frame, crash_img, [border_offset, border_offset])
    frame = cvzone.overlayPNG(frame, ride_img, [frame_w - ride_img_w - border_offset, border_offset])

    ## display Webcam (until 'q' is pressed)
    cv.imshow('Webcam', frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

## release and close everything
capture.release()
cv.destroyAllWindows()
