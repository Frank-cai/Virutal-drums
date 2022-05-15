# Virutal-drums

## Setup ##
Project created in Pycharm (Windows 10)
Make sure to install all packages (opencv-python, mediapipe, ... (see import list of main.py))
  To install packages go to "File -> Settings... -> Project: VirtualDrum -> Python Interpreter"
The projet consists out of two files (main.py and functions.py) and two folders (images and sound)


## Play Drums ##
Execute main.py to run the project (make sure that the folders are at the right place)

A gui should open showing you your webcam with drum overlays. If the window is black or showing not the right webcam, you will have to adjust the input device in main.py (line 61: capture = cv.VideoCapture(0) // see comments there)

On the right side there should also be 3 buttons and a gray box. The box is used for simon says.
Make sure to use the "Exit" button to quit.
