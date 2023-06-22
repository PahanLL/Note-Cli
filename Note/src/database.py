import base64
import psycopg2
import logging
from config import config

logging.basicConfig(filename='../logs/cms.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

class CMS:
    def __init__(self):
        self.params = config()
        self.connection = psycopg2.connect(**self.params)
        self.connect()

    def connect(self):
        try:
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to connect to the PostgreSQL database: %s', error)
            print(error)
        finally:
            if self.connection is None:
                self.connection.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def createUser(self, firstName, lastName, email, telephone):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user is not None:
                print("User already exists.")
                return logger.error('User already exists.')

            cursor.execute("INSERT INTO \"user\" (first_name, last_name, email, telephone) VALUES (%s, %s, %s, %s)", (firstName, lastName, email, telephone))
            self.connection.commit()
            print("User created successfully.")
            cursor.close()
            return "User created successfully."

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to create user: %s', error)
            print(error)

    def uploadContent(self, userEmail, title, contentType, description, filePath):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (userEmail,))
            user = cursor.fetchone()

            if user is None:
                print("User does not exist.")
                return logger.error('User does not exist.')

            with open(filePath, 'rb') as file:
                binaryData = file.read()
                encodedData = base64.b64encode(binaryData)

            # Проверка на наличие такого же файла у пользователя
            cursor.execute("SELECT * FROM content WHERE userEmail = %s AND content = %s", (userEmail, encodedData))
            existing_content = cursor.fetchone()

            if existing_content is not None:
                print("This file has already been uploaded by the user.")
                return logger.error('This file has already been uploaded by the user.')

            cursor.execute("INSERT INTO content (userEmail, title, content_type, description, content) VALUES (%s, %s, %s, %s, %s)", 
                           (userEmail, title, contentType, description, encodedData))
            self.connection.commit()
            print("Data added successfully.")
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to upload content: %s', error)
            print(error)

    def deleteUser(self, userEmail):
        try:
            cursor = self.connection.cursor()

            cursor.execute("DELETE FROM \"user\" WHERE email = %s", (userEmail,))
            cursor.execute("DELETE FROM content WHERE userEmail = %s", (userEmail,))
            self.connection.commit()
            print("User deleted successfully.")
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete user: %s', error)
            print(error)

    def deleteContent(self, contentId, userEmail):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (userEmail,))
            user = cursor.fetchone()

            if user is None:
                print("User does not exist.")
                return logger.error('User does not exist.')

            cursor.execute("SELECT * FROM content WHERE id = %s AND userEmail = %s", (contentId, userEmail))
            content = cursor.fetchone()

            if content is None:
                print("Content does not exist for this user.")
                return logger.error('Content does not exist for this user.')

            cursor.execute("DELETE FROM content WHERE id = %s AND userEmail = %s", (contentId, userEmail))
            self.connection.commit()
            print("Content deleted successfully.")
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete content: %s', error)
            print(error)
    
    def copyContent(self, sourceUserEmail, targetUserEmail, contentTitle):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (sourceUserEmail,))
            sourceUser = cursor.fetchone()

            if sourceUser is None:
                print("Source user does not exist.")
                return logger.error('Source user does not exist.')

            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (targetUserEmail,))
            targetUser = cursor.fetchone()

            if targetUser is None:
                print("Target user does not exist.")
                return logger.error('Target user does not exist.')

            cursor.execute("SELECT * FROM content WHERE title = %s AND userEmail = %s", (contentTitle, sourceUserEmail))
            content = cursor.fetchone()

            if content is None:
                print("Content does not exist for source user.")
                return logger.error('Content does not exist for source user.')

            cursor.execute("SELECT * FROM content WHERE userEmail = %s AND content = %s", (targetUserEmail, content[4]))
            existing_content = cursor.fetchone()

            if existing_content is not None:
                print("This file has already been uploaded by the target user.")
                return logger.error('This file has already been uploaded by the target user.')

            cursor.execute("INSERT INTO content (userEmail, title, content_type, description, content) VALUES (%s, %s, %s, %s, %s)",
                           (targetUserEmail, content[1], content[2], content[3], content[4]))
            self.connection.commit()
            print("Content copied successfully.")
            cursor.close()

        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to copy content: %s', error)
            print(error)