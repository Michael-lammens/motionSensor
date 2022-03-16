import pymysql # Info Here: https://pypi.org/project/PyMySQL/

db = pymysql.connect(user='root',password='',host='localhost')
mycursor = db.cursor()
mycursor.execute("CREATE DATABASE motionDetector")
