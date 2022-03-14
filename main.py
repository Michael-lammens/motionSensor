# current testing for opencv library

import numpy as Np
import cv2
import sys
import time



# webcam video detection

cap = cv2.VideoCapture(0)
ret, frame2 = cap.read()  # define frame 2 outside of function # will use this frame to compare to frame 1

# learn how to do the video save and save both an image and start recording. once it starts recording, record for 2 seconds
# break and exit back to the initial movement monitor.

# all files saved to /images can be pushed into SQL.

frameCaptured = []  # create a list of frames captured to export
imageNumber = 0 # count the number of images
count = 0 # count the number of frames
while True:

    ret, frame = cap.read()  # frame is a numpy array of the image, ret = boolean valid or not image

    diff = cv2.absdiff(frame, frame2)  # find the difference between frames
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)  # convert to grayscale
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # reduce image noise?
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  # convert the image to binary to analyze easier
    dilated = cv2.dilate(thresh, None, iterations=3)  # dilate the image, not sure why.

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:  # if the frame is large enough, lets save the images to a file
        if cv2.contourArea(contour) < 1100:
             # create new image for the frame
            print("Hello")

    cv2.imshow('frame', frame)  # display the frame

    ret, frame2 = cap.read()  # get the last frame to compare to the next

    if cv2.waitKey(1) == ord('q'):  # key to break function
        break

cap.release()
cv2.destroyAllWindows()

print(frameCaptured)
cv2.imshow('frame', frame)
# use collection of frames to create a video


# cv2.drawContours(frame, contours, -1, (0, 255, 0, 2)) # show that we are finding movement
# cv2.imwrite('images/image{}.jpg'.format(count),frame2