import cv2 as cv
import mediapipe as mp
import time
import cvzone
from functions import image_config
from functions import gesture
import pygame

## pathes
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

## image positions
Top_Left = 1
Top_Right = 2
Bottom_Left = 3
Bottom_Middle = 4
Bottom_Right = 5

## used for fps
previousTime = 0
currentTime = 0

## captures Webcam (may have to put another integer than 0 if you do not see through the wanted device)
capture = cv.VideoCapture(0, cv.CAP_DSHOW)

## image positions (top left = tl // bottom right = br)
border_offset = 10
isTrue, frame = capture.read()
frame_h, frame_w, frame_c = frame.shape

ride_img, ride_img_tl_x, ride_img_tl_y, ride_img_br_x, ride_img_br_y = image_config(image_ride_path, frame_w, frame_h, border_offset, Top_Left)
crash_img, crash_img_tl_x, crash_img_tl_y, crash_img_br_x, crash_img_br_y = image_config(image_crash_path, frame_w, frame_h, border_offset, Top_Right)
snare_img, snare_img_tl_x, snare_img_tl_y, snare_img_br_x, snare_img_br_y = image_config(image_snare_path, frame_w, frame_h, border_offset, Bottom_Left)
bass_img, bass_img_tl_x, bass_img_tl_y, bass_img_br_x, bass_img_br_y = image_config(image_bass_path, frame_w, frame_h, border_offset, Bottom_Middle)
tom_img, tom_img_tl_x, tom_img_tl_y, tom_img_br_x, tom_img_br_y = image_config(image_tom_path, frame_w, frame_h, border_offset, Bottom_Right)

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
            flag = gesture(handLms, joint_list)
            if flag:
                if ride_img_tl_y < handLms.landmark[12].y*frame_h < ride_img_br_y and ride_img_tl_x < handLms.landmark[12].x*frame_w < ride_img_br_x:
                    if position != Top_Left:
                        ride_sound.play()
                    position = Top_Left
                elif crash_img_tl_y < handLms.landmark[12].y*frame_h < crash_img_br_y and crash_img_tl_x < handLms.landmark[12].x*frame_w < crash_img_br_x:
                    if position != Top_Right:
                        crash_sound.play()
                    position = Top_Right
                elif snare_img_tl_y < handLms.landmark[12].y*frame_h < snare_img_br_y and snare_img_tl_x < handLms.landmark[12].x*frame_w < snare_img_br_x:
                    if position != Bottom_Left:
                        snare_sound.play()
                    position = Bottom_Left
                elif bass_img_tl_y < handLms.landmark[12].y*frame_h < bass_img_br_y and bass_img_tl_x < handLms.landmark[12].x*frame_w < bass_img_br_x:
                    if position != Bottom_Middle:
                        bass_sound.play()
                    position = Bottom_Middle
                elif tom_img_tl_y < handLms.landmark[12].y*frame_h < tom_img_br_y and tom_img_tl_x < handLms.landmark[12].x*frame_w < tom_img_br_x:
                    if position != Bottom_Right:
                        tom_sound.play()
                    position = Bottom_Right
                else:
                    position = 0

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    ## add fps to webcam
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv.putText(frame, str(int(fps)), (int(frame_w / 2 - frame_w / 10), 80), cv.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 0), 3)

    ## add drum parts to webcam
    frame = cvzone.overlayPNG(frame, snare_img, [snare_img_tl_x, snare_img_tl_y])
    frame = cvzone.overlayPNG(frame, tom_img, [tom_img_tl_x, tom_img_tl_y])
    frame = cvzone.overlayPNG(frame, bass_img, [bass_img_tl_x, bass_img_tl_y])
    frame = cvzone.overlayPNG(frame, crash_img, [crash_img_tl_x, crash_img_tl_y])
    frame = cvzone.overlayPNG(frame, ride_img, [ride_img_tl_x, ride_img_tl_y])

    cv.rectangle(frame, (snare_img_tl_x, snare_img_tl_y), (snare_img_br_x, snare_img_br_y), (255, 255, 0), 1)
    cv.rectangle(frame, (tom_img_tl_x, tom_img_tl_y), (tom_img_br_x, tom_img_br_y), (255, 255, 0), 1)
    cv.rectangle(frame, (bass_img_tl_x, bass_img_tl_y), (bass_img_br_x, bass_img_br_y), (255, 255, 0), 1)
    cv.rectangle(frame, (crash_img_tl_x, crash_img_tl_y), (crash_img_br_x, crash_img_br_y), (255, 255, 0), 1)
    cv.rectangle(frame, (ride_img_tl_x, ride_img_tl_y), (ride_img_br_x, ride_img_br_y), (255, 255, 0), 1)

    ## display Webcam (until 'q' is pressed)
    cv.imshow('Webcam', frame)
    if cv.waitKey(20) & 0xFF == ord('q'):
        break

## release and close everything
capture.release()
cv.destroyAllWindows()
