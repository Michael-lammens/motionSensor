import pymysql # Info Here: https://pypi.org/project/PyMySQL/

db = pymysql.connect(user='root',password='',host='localhost',database='motionDetector')
mycursor = db.cursor()
mycursor.execute("CREATE TABLE Images (name VARCHAR(50),time smallint UNSIGNED)")
