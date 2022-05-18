import cv2 as cv
import mediapipe as mp
import time
import cvzone
import numpy as np
from functions import get_label

from functions import image_config
from functions import gesture
from functions import image_resize
import pygame
from tkinter import *
from PIL import Image, ImageTk
from random import randrange

## global variables
run_loop = True
run_game = False
simon_says = ""
user_replies = ""
SIMON_ADD_COLOR = False

## paths
icon_drum_path = "images/icon.ico"

image_ride_path = "images/ride.png"
image_crash_path = "images/crash.png"
image_snare_path = "images/snare.png"
image_bass_path = "images/bass.png"
image_tom_path = "images/tom.png"

sound_ride_path = "sound/hihat.mp3"
sound_crash_path = "sound/cymbal.mp3"
sound_snare_path = "sound/drum_snare.mp3"
sound_bass_path = "sound/drum_bass.mp3"
sound_tom_path = "sound/drum_tom1.mp3"

## image positions
Top_Left = 1
Top_Right = 2
Bottom_Left = 3
Bottom_Middle = 4
Bottom_Right = 5

## used for fps
previousTime = 0
currentTime = 0

## used for tkinter gui
gui_width_addition = 250
gui_height_addition = 100

## used for simon says
step = 0
simon_currentTime = 0
simon_startTime = 0
USERS_TURN = False

## captures Webcam (may have to put another integer than 0 if you do not see through the wanted device)
# capture = cv.VideoCapture(0, cv.CAP_DSHOW)
capture = cv.VideoCapture(0)

## image positions (top left = tl // bottom right = br)
border_offset = 30
isTrue, frame = capture.read()
frame = image_resize(frame, height=720)
frame_h, frame_w, frame_c = frame.shape
print(frame.shape)

ride_img, ride_img_tl_x, ride_img_tl_y, ride_img_br_x, ride_img_br_y = image_config(image_ride_path, frame_w, frame_h, border_offset, Top_Left)
crash_img, crash_img_tl_x, crash_img_tl_y, crash_img_br_x, crash_img_br_y = image_config(image_crash_path, frame_w, frame_h, border_offset, Top_Right)
snare_img, snare_img_tl_x, snare_img_tl_y, snare_img_br_x, snare_img_br_y = image_config(image_snare_path, frame_w, frame_h, border_offset, Bottom_Left)
bass_img, bass_img_tl_x, bass_img_tl_y, bass_img_br_x, bass_img_br_y = image_config(image_bass_path, frame_w, frame_h, border_offset, Bottom_Middle)
tom_img, tom_img_tl_x, tom_img_tl_y, tom_img_br_x, tom_img_br_y = image_config(image_tom_path, frame_w, frame_h, border_offset, Bottom_Right)

## read sound files
pygame.mixer.init()
ride_sound = pygame.mixer.Sound(sound_ride_path)
crash_sound = pygame.mixer.Sound(sound_crash_path)
snare_sound = pygame.mixer.Sound(sound_snare_path)
bass_sound = pygame.mixer.Sound(sound_bass_path)
tom_sound = pygame.mixer.Sound(sound_tom_path)

## initialize a hand object
mpHands = mp.solutions.hands
hands = mpHands.Hands(2)  # set the maximum number of hands to 2
mpDraw = mp.solutions.drawing_utils
position = [0, 0]  # [left hand, right hand]
joint_list = [[5, 6, 7], [9, 10, 11], [13, 14, 15], [17, 18, 19]]

### tkinter GUI ###
tkinter_width = str(frame_w + gui_width_addition)
tkinter_height = str(frame_h + gui_height_addition)

root = Tk()
root.title("Virtual Drum")
root.iconbitmap(icon_drum_path)
root.geometry(tkinter_width+"x"+tkinter_height)

## Titel and Webcam
webcam_label = Label(root, text="Virtual Drum", font=("times new roman", 30, "bold"))
webcam_label.grid(row=0, column=4)
webcam_frame = Label(root, bg="black")
webcam_frame.grid(row=1, column=0, rowspan=10, columnspan=10, padx=50)


## functions for buttons
def freePlay():
    global run_game
    run_game = False
    game_text.set("Free Play")


def startGame():
    global run_game
    global SIMON_ADD_COLOR
    global simon_says
    global user_replies
    global step
    run_game = True
    SIMON_ADD_COLOR = True
    simon_says = ""
    user_replies = ""
    step = 0
    game_text.set("Remember what\nsimon says")


def quitGUi():
    global run_loop
    run_loop = False
    capture.release()
    root.destroy()


## buttons
freeplay_button = Button(root, text="Free Play", command=freePlay, width=10)
freeplay_button.grid(row=1, column=10)
Game_button = Button(root, text="Start Game", command=startGame, width=10)
Game_button.grid(row=3, column=10)
exit_button = Button(root, text="Exit", command=quitGUi, width=10)
exit_button.grid(row=10, column=10)

### simon says images
gray_img = Image.new(mode="RGB", size=(100, 100), color=(211, 211, 211))
gray_img = ImageTk.PhotoImage(gray_img)
green_img = Image.new(mode="RGB", size=(100, 100), color=(0, 255, 0))
green_img = ImageTk.PhotoImage(green_img)
blue_img = Image.new(mode="RGB", size=(100, 100), color=(0, 0, 255))
blue_img = ImageTk.PhotoImage(blue_img)
red_img = Image.new(mode="RGB", size=(100, 100), color=(255, 0, 0))
red_img = ImageTk.PhotoImage(red_img)
cyan_img = Image.new(mode="RGB", size=(100, 100), color=(0, 255, 255))
cyan_img = ImageTk.PhotoImage(cyan_img)
purple_img = Image.new(mode="RGB", size=(100, 100), color=(255, 0, 255))
purple_img = ImageTk.PhotoImage(purple_img)

simon_img = gray_img
simon_frame = Label(bg="black")
simon_frame.grid(row=4, column=10)

## simon says text
game_text = StringVar()
game_text.set("Welcome to\nVirtual Drum")
simon_text = Label(root, textvariable=game_text, font=("Arial", 10))
simon_text.grid(row=5, column=10)

while run_loop:
    ## capture Webcam frames
    isTrue, frame = capture.read()
    frame = image_resize(frame, height=720)
    frame = cv.flip(frame, 1)

    ## process hands (currently maximum amount of hands is 2; if you want more or less hands see 'initialize a hand object' mpHands.Hands())
    frameRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frameRGB)

    ## generate landmarks on hands
    # print(results.multi_hand_landmarks)
    if results.multi_hand_landmarks:
        for num, handLms in enumerate(results.multi_hand_landmarks):
            flag, LR = gesture(handLms, joint_list, num, results)
            # show left and right-hand label
            if get_label(num, handLms, results, frame.shape[1], frame.shape[0]):
                text, coord = get_label(num, handLms, results, frame.shape[1], frame.shape[0])
                cv.putText(frame, text, coord, cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)

            if flag:
                if ride_img_tl_y < handLms.landmark[8].y * frame_h < ride_img_br_y and ride_img_tl_x < handLms.landmark[8].x * frame_w < ride_img_br_x:
                    if position[LR] != Top_Left:
                        ride_sound.play()
                        if USERS_TURN:
                            user_replies += str(Top_Left)
                    position[LR] = Top_Left
                elif crash_img_tl_y < handLms.landmark[8].y * frame_h < crash_img_br_y and crash_img_tl_x < handLms.landmark[8].x * frame_w < crash_img_br_x:
                    if position[LR] != Top_Right:
                        crash_sound.play()
                        if USERS_TURN:
                            user_replies += str(Top_Right)
                    position[LR] = Top_Right
                elif snare_img_tl_y < handLms.landmark[8].y * frame_h < snare_img_br_y and snare_img_tl_x < handLms.landmark[8].x * frame_w < snare_img_br_x:
                    if position[LR] != Bottom_Left:
                        snare_sound.play()
                        if USERS_TURN:
                            user_replies += str(Bottom_Left)
                    position[LR] = Bottom_Left
                elif bass_img_tl_y < handLms.landmark[8].y * frame_h < bass_img_br_y and bass_img_tl_x < handLms.landmark[8].x * frame_w < bass_img_br_x:
                    if position[LR] != Bottom_Middle:
                        bass_sound.play()
                        if USERS_TURN:
                            user_replies += str(Bottom_Middle)
                    position[LR] = Bottom_Middle
                elif tom_img_tl_y < handLms.landmark[8].y * frame_h < tom_img_br_y and tom_img_tl_x < handLms.landmark[8].x * frame_w < tom_img_br_x:
                    if position[LR] != Bottom_Right:
                        tom_sound.play()
                        if USERS_TURN:
                            user_replies += str(Bottom_Right)
                    position[LR] = Bottom_Right
                else:
                    position[LR] = 0

            mpDraw.draw_landmarks(frame, handLms, mpHands.HAND_CONNECTIONS)

    ## add fps to webcam
    currentTime = time.time()
    fps = 1 / (currentTime - previousTime)
    previousTime = currentTime
    cv.putText(frame, str(int(fps)), (int(frame_w / 2 - frame_w / 15), 80), cv.FONT_HERSHEY_TRIPLEX, 3, (0, 255, 0), 3)

    ## add drum parts to webcam
    frame = cvzone.overlayPNG(frame, ride_img, [ride_img_tl_x, ride_img_tl_y])
    frame = cvzone.overlayPNG(frame, crash_img, [crash_img_tl_x, crash_img_tl_y])
    frame = cvzone.overlayPNG(frame, snare_img, [snare_img_tl_x, snare_img_tl_y])
    frame = cvzone.overlayPNG(frame, bass_img, [bass_img_tl_x, bass_img_tl_y])
    frame = cvzone.overlayPNG(frame, tom_img, [tom_img_tl_x, tom_img_tl_y])

    cv.rectangle(frame, (ride_img_tl_x, ride_img_tl_y), (ride_img_br_x, ride_img_br_y), (0, 255, 0), 2)
    cv.rectangle(frame, (crash_img_tl_x, crash_img_tl_y), (crash_img_br_x, crash_img_br_y), (255, 0, 0), 2)
    cv.rectangle(frame, (snare_img_tl_x, snare_img_tl_y), (snare_img_br_x, snare_img_br_y), (0, 0, 255), 2)
    cv.rectangle(frame, (bass_img_tl_x, bass_img_tl_y), (bass_img_br_x, bass_img_br_y), (255, 255, 0), 2)
    cv.rectangle(frame, (tom_img_tl_x, tom_img_tl_y), (tom_img_br_x, tom_img_br_y), (255, 0, 255), 2)

    ## simon says
    if run_game:
        simon_currentTime = time.time()

        ## add color
        if SIMON_ADD_COLOR:
            simon_says += str(randrange(5) + 1)
            SIMON_ADD_COLOR = False
            # print(simon_says)
            simon_startTime = simon_currentTime
            USERS_TURN = False

        ## show color(s)
        if simon_currentTime - simon_startTime >= 1:
            if simon_img == gray_img and len(simon_says) > step:
                if int(simon_says[step]) == 1:
                    simon_img = green_img
                    ride_sound.play()
                elif int(simon_says[step]) == 2:
                    simon_img = blue_img
                    crash_sound.play()
                elif int(simon_says[step]) == 3:
                    simon_img = red_img
                    snare_sound.play()
                elif int(simon_says[step]) == 4:
                    simon_img = cyan_img
                    bass_sound.play()
                elif int(simon_says[step]) == 5:
                    simon_img = purple_img
                    tom_sound.play()
                step = step + 1
                simon_startTime = simon_currentTime
            else:
                simon_img = gray_img
                if len(simon_says) != step:
                    simon_startTime = simon_currentTime

        ## start recognizing user input
        if simon_currentTime - simon_startTime >= 2 and len(simon_says) == step:
            game_text.set("Repeat")
            USERS_TURN = True

        ## determine simon says result
        for i in range(0, len(user_replies)):
            if user_replies[i] != simon_says[i]:
                run_game = False
                game_text.set(f"Game over\nYour score: {len(simon_says) - 1}")
                simon_says = ""

        if len(user_replies) == len(simon_says):
            if simon_says != user_replies:
                run_game = False
                game_text.set(f"Game over\nYour score: {len(simon_says)-1}")
                simon_says = ""
            else:
                game_text.set("Correct. Remember\nwhat simon says")
                SIMON_ADD_COLOR = True
            user_replies = ""
            step = 0
    else:
        simon_img = gray_img

    ## display Webcam
    webcam_img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    webcam_img = ImageTk.PhotoImage(Image.fromarray(webcam_img))
    webcam_frame['image'] = webcam_img

    ## display simon says image
    simon_frame['image'] = simon_img

    ## update gui
    root.update()
