import psycopg2
import logging
from config import config

logging.basicConfig(filename='../logs/note.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.params = config()
        self.connect()

    def connect(self):
        try:
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.params)
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to connect to the PostgreSQL database: %s', error)
        finally:
            if self.connection is None:
                self.connection.close()

    def close(self):
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    # Users

    def createUser(self, name, email, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM \"user\" WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user is not None:
                return logger.error('User already exists.')
            cursor.execute("INSERT INTO \"user\" (name, email, password) VALUES (%s, %s, %s)", (name, email, password))
            self.connection.commit()
            cursor.close()
            return "User created successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to create user: %s', error)

    def deleteUser(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM \"user\" WHERE user_id = %s", (user_id,))
            self.connection.commit()
            cursor.close()
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete user: %s', error)

    def login(self, email, password):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM \"user\" WHERE email = %s AND password = %s", (email, password))
            user = cursor.fetchone()
            if user is None:
                return logger.error('Login failed.')
            cursor.close()
            return user
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to login: %s', error)

    # Notes

    def createNote(self, title, content, user_id, category_ids=None):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO note (title, content, user_id) VALUES (%s, %s, %s) RETURNING note_id",
                           (title, content, user_id))
            note_id = cursor.fetchone()[0]

            if category_ids is not None:
                for category_id in category_ids:
                    cursor.execute("INSERT INTO note_category (note_id, category_id) VALUES (%s, %s)",
                                   (note_id, category_id))
            
            self.connection.commit()
            cursor.close()
            return "Note created successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to create note: %s', error)
            return "Note creation failed."

    def filterNotesByDate(self, start_date, end_date):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM note WHERE created_at BETWEEN %s AND %s", (start_date, end_date))
            notes = cursor.fetchall()
            cursor.close()
            return notes
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to filter notes by date: %s', error)

    def updateNote(self, note_id, title=None, content=None, category_ids=None):
        try:
            cursor = self.connection.cursor()

            if title is not None:
                cursor.execute("UPDATE note SET title = %s WHERE note_id = %s", (title, note_id))
            else:
                cursor.execute("UPDATE note SET title = NULL WHERE note_id = %s", (note_id,))
            
            if content is not None:
                cursor.execute("UPDATE note SET content = %s WHERE note_id = %s", (content, note_id))
            else:
                cursor.execute("UPDATE note SET content = NULL WHERE note_id = %s", (note_id,))

            if category_ids is not None:
                # Удаление связей существующих категорий
                cursor.execute("DELETE FROM note_category WHERE note_id = %s", (note_id,))
                
                # Добавление новых связей категорий
                for category_id in category_ids:
                    if category_id:
                        cursor.execute("SELECT EXISTS(SELECT 1 FROM category WHERE category_id = %s)", (category_id,))
                        category_exists = cursor.fetchone()[0]
                        if category_exists:
                            cursor.execute("INSERT INTO note_category (note_id, category_id) VALUES (%s, %s)",
                                        (note_id, category_id))
                        else:
                            logger.error('Category with ID %s does not exist. Skipping...', category_id)
                    else:
                        logger.error('Invalid category ID. Skipping...')

            self.connection.commit()
            cursor.close()
            return "Note updated successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to update note: %s', error)

    def deleteNote(self, note_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM note WHERE note_id = %s", (note_id,))
            self.connection.commit()
            cursor.close()
            return "Note deleted successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete note: %s', error)
            return "Note does not exist."

    def getNote(self, note_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM note WHERE note_id = %s", (note_id,))
            note = cursor.fetchone()
            if note is None:
                return "Note not found."
            
            cursor.execute("SELECT category_id FROM note_category WHERE note_id = %s", (note_id,))
            categories = cursor.fetchall()
            
            cursor.close()
            return note, categories
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to get note: %s', error)

    def getAllNotes(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM note WHERE user_id = %s", (user_id,))
            notes = cursor.fetchall()
            cursor.close()
            return notes
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to get all notes: %s', error)

    def searchNoteByTitle(self, title, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM note WHERE title = %s AND user_id = %s", (title, user_id))
            notes = cursor.fetchall()
            cursor.close()
            return notes
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to search notes by title: %s', error)

    # Categories

    def createCategory(self, name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO category (name) VALUES (%s) RETURNING category_id", (name,))
            category_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return f"Category created successfully. Category ID: {category_id}"
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to create category: %s', error)
            return "Failed to create category."

    def deleteCategory(self, category_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM category WHERE category_id = %s", (category_id,))
            self.connection.commit()
            cursor.close()
            return "Category deleted successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete category: %s', error)
            return "Category does not exist."

    # Groups

    def createGroup(self, name):
        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO \"group\" (name) VALUES (%s)", (name,))
            self.connection.commit()
            cursor.close()
            return "Group created successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to create group: %s', error)

    def getAllGroups(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM \"group\"")
            groups = cursor.fetchall()
            cursor.close()
            return groups
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to get all groups: %s', error)

    def deleteGroup(self, group_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM \"group\" WHERE group_id = %s", (group_id,))
            self.connection.commit()
            cursor.close()
            return "Group deleted successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to delete group: %s', error)
            return "Group does not exist."

    def getNotesInGroup(self, group_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT note.* FROM note "
                           "INNER JOIN note_group ON note.note_id = note_group.note_id "
                           "WHERE note_group.group_id = %s", (group_id,))
            notes = cursor.fetchall()
            cursor.close()
            return notes
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to get notes in group: %s', error)

    def addNoteToGroup(self, note_id, group_id):
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SELECT * FROM note WHERE note_id = %s", (note_id,))
            note = cursor.fetchone()
            if note is None:
                return "Note does not exist."
            
            cursor.execute("SELECT * FROM \"group\" WHERE group_id = %s", (group_id,))
            group = cursor.fetchone()
            if group is None:
                return "Group does not exist."
            
            cursor.execute("INSERT INTO note_group (note_id, group_id) VALUES (%s, %s)", (note_id, group_id))
            self.connection.commit()
            
            cursor.close()
            return "Note added to group successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to add note to group: %s', error)

    def assignCategoryToNote(self, note_id, category_id):
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT * FROM note WHERE note_id = %s", (note_id,))
            note = cursor.fetchone()
            if note is None:
                return "Note does not exist."

            cursor.execute("SELECT * FROM category WHERE category_id = %s", (category_id,))
            category = cursor.fetchone()
            if category is None:
                return "Category does not exist."

            cursor.execute("SELECT * FROM note_category WHERE note_id = %s AND category_id = %s", (note_id, category_id))
            existing_relation = cursor.fetchone()
            if existing_relation is not None:
                return "Category is already assigned to the note."

            cursor.execute("INSERT INTO note_category (note_id, category_id) VALUES (%s, %s)", (note_id, category_id))
            self.connection.commit()

            cursor.close()
            return "Category assigned to note successfully."
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to assign category to note: %s', error)

    def getNoteCategories(self, note_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT category.name FROM category "
                           "JOIN note_category ON category.category_id = note_category.category_id "
                           "WHERE note_category.note_id = %s", (note_id,))
            categories = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return categories
        except (Exception, psycopg2.DatabaseError) as error:
            logger.error('Failed to get categories for note: %s', error)
