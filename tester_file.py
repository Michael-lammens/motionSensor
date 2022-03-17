
import pymysql

db = pymysql.connect(user='root',password='password',host='localhost', database="motionDetector")
mycursor = db.cursor()

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




retreive_video(3)

