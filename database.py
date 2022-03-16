import pymysql #Download Here: https://pypi.org/project/PyMySQL/

db = pymysql.connect(user='root',password='',host='localhost') #,database='motionDetector'
mycursor = db.cursor()

            # Create database if not already defined
#mycursor.execute("CREATE DATABASE motionDetector")

            # Creates new table "Images" with the following values
#mycursor.execute("CREATE TABLE Images (name VARCHAR(50),time smallint UNSIGNED)")

            # adds values into the database and commits the change
#mycursor.execute("INSERT INTO Images(name, time) VALUES (%s,%s)",("image0",1920))
#db.commit()
