import cv2 as cv
import vlc


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


if __name__ == '__main__':
    camera()

