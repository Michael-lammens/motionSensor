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
        mycursor.execute("CREATE TABLE Images (time VARCHAR(20), thumbnail LONGBLOB, video LONGBLOB, id int PRIMARY KEY AUTO_INCREMENT )")
        db.commit()
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
    output = cv2.VideoWriter('images/output{}.avi'.format(vid_num), cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20, frame_size)
    start = time.time() # get the start time
    print("RECORDING*")
    while True:
        ret, frame = cap.read()  # frame is a numpy array of the image, ret = boolean valid or not image
        cv2.imshow('frame', frame)  # display the frame

        output.write(frame) # write to our video
        thumbnail = cv2.imwrite('images/image{}.png'.format(vid_num),frame)
        file_path = ('images/image{}.png'.format(vid_num))


        if cv2.waitKey(1) == ord('q'):  # key to break function
            cap.release()
            cv2.destroyAllWindows()
            output.release()
            exit()

        if time.time() -start > 10:
            print("RECORDING DONE", vid_num)
            output.release()
            # get video path
            video_path = ("images/output{}.avi".format(vid_num))
            # push to database
            push_data(file_path,video_path)

            mainThread(vid_num)

# create function to push all data to sql

def push_data(photoPath, videoPath):
    """

    :param time: Time of the video taken ***
    :param image: Thumbnail of video, first frame # file path
    :param video: Video file
    :param name: video{vid_num}
    :return: Status
    """

        # convert the image to binary to push
    with open(photoPath, "rb") as File:
        binaryImgData = File.read()
        # convert the video to binary to push
    with open(videoPath, "rb") as File:
        binaryVideoData = File.read()

        # get the current time to push
    t = time.localtime()
    currentTime = time.strftime("%H:%M:%S", t)

        # push to sql
    sql_statement = "INSERT INTO Images (time, thumbnail, video) VALUES (%s,%s,%s)"
    mycursor.execute(sql_statement, (currentTime, binaryImgData, binaryVideoData))
    db.commit()


mainThread(video_num)







# function for testing or if we ever need to return a particular video by id. No use right now
def retreive_video(id):
    """
    Create a local file with the video contents by the videos database id number
    :param id:
    :return:
    """
    sqlstatement = "SELECT video FROM Images WHERE id = '{0}'"
    mycursor.execute(sqlstatement.format(id))
    result = mycursor.fetchone()[0]
    storefile = "returnedVideo.mp4"
    with open(storefile, "wb") as File:
        File.write(result)
        File.close()

