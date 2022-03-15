# current testing for opencv library

import numpy as Np
import cv2
import sys
import time



# webcam video detection

cap = cv2.VideoCapture(0)
ret, frame2 = cap.read()  # define frame 2 outside of function # will use this frame to compare to frame 1

# get the size of the video

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)




# learn how to do the video save and save both an image and start recording. once it starts recording, record for 2 seconds
# break and exit back to the initial movement monitor.

# all files saved to /images can be pushed into SQL.


#*****
# Now find a way to trigger a function that starts recording after the first detected movement for 20 seconds
# once 20 seconds has passed, return the recording. continue looking for movement from where we left of


output = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 20, frame_size)
start = time.time()
while True:


    ret, frame = cap.read()  # frame is a numpy array of the image, ret = boolean valid or not image

    diff = cv2.absdiff(frame, frame2)  # find the difference between frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # reduce image noise?
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # convert the image to binary to analyze easier
    dilated = cv2.dilate(thresh, None, iterations=3)  # dilate the image, not sure why.

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) > 900:
             # start video capture,
            output.write(frame)
            print("start recording now")


    cv2.imshow('frame', frame)  # display the frame
    ret, frame2 = cap.read()  # get the last frame to compare to the next

    if cv2.waitKey(1) == ord('q'):  # key to break function
        break

cap.release()
output.release()
cv2.destroyAllWindows()

stop = time.time()
print(stop-start)

