import psycopg2
from config import config


class Database:
    @staticmethod
    def migrate():
        commands = (
            """
            CREATE TABLE "user" (
                user_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL,
                email varchar(100) NOT NULL UNIQUE,
                password varchar(50) NOT NULL
            );
            CREATE TABLE note (
                note_id SERIAL PRIMARY KEY,
                title varchar(100) NOT NULL,
                content text NOT NULL,
                user_id INT REFERENCES "user" (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE category (
                category_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL
            );
            CREATE TABLE "group" (
                group_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL
            );
            CREATE TABLE note_category (
                note_id INT REFERENCES note (note_id) ON UPDATE CASCADE ON DELETE CASCADE,
                category_id INT REFERENCES category (category_id) ON UPDATE CASCADE ON DELETE CASCADE,
                PRIMARY KEY (note_id, category_id)
            );
            CREATE TABLE note_group (
                note_id INT REFERENCES note (note_id) ON UPDATE CASCADE ON DELETE CASCADE,
                group_id INT REFERENCES "group" (group_id) ON UPDATE CASCADE ON DELETE CASCADE,
                PRIMARY KEY (note_id, group_id)
            );
            """
        )

        conn = None
        try:
            params = config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            cur.execute(commands)

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


if __name__ == '__main__':
    Database.migrate()
