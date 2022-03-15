import mysql.connector

# connect to database
db = mysql.connector.connect(
    host= "localhost",
    user ="root",
    passwd="password",
    database = "motionDetector" # comment this out and run the "CREATE DATABASE" method if yours isnt defined.
                                # then add it back
)

mycursor = db.cursor()







            # Create database if not already defined
#mycursor.execute("CREATE DATABASE motionDetector)

            # Creates new table "Images" with the following values
#mycursor.execute("CREATE TABLE Images (name VARCHAR(50),time smallint UNSIGNED)")

            # adds values into the database and commits the change
#mycursor.execute("INSERT INTO Images(name, time) VALUES (%s,%s)",("image0",1920))
#db.commit()
