# current testing for opencv library

import numpy as Np
import cv2
import sys
import time
import pymysql

# maintain db connection

# assuming the first run will not be connected. Create connection

try:
    db = pymysql.connect(user='root',password='password',host='localhost',database="motionDetector")
    mycursor = db.cursor() # stays global
except:
    print("Establishing database connection...")
    try:
        db = pymysql.connect(user='root', password='password', host='localhost')
        mycursor = db.cursor()
        mycursor.execute("CREATE DATABASE motionDetector")
        db = pymysql.connect(user='root', password='password', host='localhost',database="motionDetector")
        # redefine db var and add tables
        mycursor = db.cursor()
        mycursor.execute("CREATE TABLE Images (name VARCHAR(50),time smallint UNSIGNED)")
    except:
        print("Error creating database...")


cap = cv2.VideoCapture(0) # start video capture
ret, frame2 = cap.read()  # define frame 2 outside of function # will use this frame to compare to frame 1

# get the size of the video

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
frame_size = (frame_width,frame_height)


#*****
#TODO create text box at top corner to indicate if its recording or not.
#TODO create a pushToDatabase function that pushes all new recording files to SQL


video_num = 0
def mainThread(vid_num):

    ret, frame2 = cap.read() # define frame 2
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
                 # call record function
                record(vid_num)

        cv2.imshow('frame', frame)  # display the frame

        ret, frame2 = cap.read()  # get the last frame to compare to the next
        if cv2.waitKey(1) == ord('q'):  # key to break function
            cap.release()
            cv2.destroyAllWindows()
            exit()


def record(vid_num):
    """
    Purpose: Once movement was detected, this function starts recording and writes to a new file after x seconds
        of recording
        Once recording is done, return back to our main thread to look for new movement.
    :param vid_num: count the number of times this function has been run(track the next files name)
    :return: None
    """
    vid_num +=1
    output = cv2.VideoWriter('Images/output{}.avi'.format(vid_num), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    start = time.time() # get the start time
    print("RECORDING*")
    while True:
        ret, frame = cap.read()  # frame is a numpy array of the image, ret = boolean valid or not image
        cv2.imshow('frame', frame)  # display the frame

        output.write(frame) # write to our video


        if cv2.waitKey(1) == ord('q'):  # key to break function
            cap.release()
            cv2.destroyAllWindows()
            output.release()
            exit()

        if time.time() -start > 10:
            print("RECORDING DONE", vid_num)
            output.release()
            mainThread(vid_num)




print("Main gets run")
mainThread(video_num)

