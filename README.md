# Virtual Drums

## Setup ##
Project created in PyCharm (Windows 10) with Python version 3.10.4.
Make sure to install all python interpreter (opencv-python, mediapipe, numpy, ... (see import list of main.py/functions.py))
  To install interpreter, go to "File -> Settings... -> Project: [name] -> Python Interpreter"
The project consists out of two files (main.py and functions.py) and two folders (images and sounds)


## Play Drums ##
Execute main.py to run the project (make sure that the folders are at the same level as the python files)

A GUI opens showing you your webcam with drum overlays. If the window is black or showing not the right webcam, you will have to adjust the input device (see "Code Instructions" below)

On the right side there are three buttons and a gray box.
The first button "Free Play" will let you play freely.
The second button "Start Game" will start a game called Simon says. In this game you must remember a given sequence which is shown in the box below the button and can also be heard. In addition, there is also a text box which shows you the status of your drum or gives you instructions like "Repeat".
The last button "Exit" will close the window. Try to always use this button to properly shut down the program.


## Code Instructions ##
The code is divided into two files (main.py and functions.py).

main.py is structured as follows:
 - path definitions
 - various definitions to make the code clearer later (e.g., image position numbers)
 - webcam capture (only the first frame) (You can adjust your webcam input device here (line 60))
 - drum image configurations
 - drum sound configurations
 - hand object initialization
 - GUI
    - geometry
    - buttons
    - Simon says images / text box
 - loop
    - capture webcam frame
    - process hands
       - find hands
       - get landmarks of hands (landmarks correspond to joints)
       - determine position and play sounds if required
    - add fps / drum images / rectangles around drum images to the webcam frame
    - Simon says
       - add color
       - show color(s)
       - compare user input with given sequence
    - display webcam / Simon says

functions.py concludes helper functions for main.py. These are:
 - gesture(hand, joint_list, index, results) - determines if your index finger is stretched (e.g., if you make a fist, you won't play a sound)
 - image_resize(image, width=None, height=None, inter=cv.INTER_AREA) - resizes an image without destroying the ratio (if only given width or height)
 - image_config(image_path, frame_w, frame_h, border_offset, image_desired_position) - resizes an image and returns coordinates of the desired position of it
 - get_label(index, hand, results, width, height) - labels your hand with left or right in the webcam frame