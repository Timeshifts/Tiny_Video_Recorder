import cv2 as cv
import datetime

camera = cv.VideoCapture(0)

# Check if the camera is opened
assert camera.isOpened(), 'Cannot open the camera'

# Get FPS and calculate the waiting time in millisecond
fps = camera.get(cv.CAP_PROP_FPS)
wait_msec = int(1 / fps * 1000)

isRecording = False
showCross = False
record_format = 'avi'
record_fourcc = 'XVID'
target = None
timestamp = ''

while True:
    # Read an image from 'video'
    valid, img = camera.read()
    h, w, *_ = img.shape

    if showCross:
        cv.line(img, (0, (int)(h/2)), (w, (int)(h/2)), (255, 255, 255), 2)
        cv.line(img, ((int)(w/2), 0), ((int)(w/2), h), (255, 255, 255), 2)

    if not valid:
        break

    if isRecording:
        target.write(img)

        # Draw a red circle and 'REC' text at the top-left of the screen
        cv.circle(img, (50, 50), 25, (0, 0, 255), -1)
        cv.circle(img, (50, 50), 25, (0, 0, 0), 2)
        cv.putText(img, "REC", (80, 70), cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 0), 7)
        cv.putText(img, "REC", (80, 70), cv.FONT_HERSHEY_DUPLEX, 2, (0, 0, 255), 3)

    # Show the image
    cv.imshow('Video Recorder', img)

    # Terminate if the given key is ESC
    key = cv.waitKey(wait_msec)
    if key == 27: # ESC
        break
    elif key == ord(' '): # Space key
        if isRecording: # REC -> no REC
            target.release()

        else: # no REC -> REC
            target = cv.VideoWriter()
            # Open the target video file
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            target_file = f'data/Record_{timestamp}.{record_format}'
            is_color = (img.ndim > 2) and (img.shape[2] > 1)
            target.open(target_file, cv.VideoWriter_fourcc(*record_fourcc), fps, (w, h), is_color)
            
        isRecording = not isRecording

    elif key == ord('c'):
        showCross = not showCross

cv.destroyAllWindows()