import psycopg2
from config import config


class CMS:
    @staticmethod
    def migrate():
        commands = (
            """
            CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL,
                email varchar(100) NOT NULL UNIQUE,
                password varchar(50) NOT NULL
            );
            CREATE TABLE notes (
                note_id SERIAL PRIMARY KEY,
                title varchar(100) NOT NULL,
                content text NOT NULL,
                user_id INT REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE
            );
            CREATE TABLE categories (
                category_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL
            );
            CREATE TABLE groups (
                group_id SERIAL PRIMARY KEY,
                name varchar(50) NOT NULL
            );
            CREATE TABLE note_category (
                note_id INT REFERENCES notes (note_id) ON UPDATE CASCADE ON DELETE CASCADE,
                category_id INT REFERENCES categories (category_id) ON UPDATE CASCADE ON DELETE CASCADE,
                PRIMARY KEY (note_id, category_id)
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
    CMS.migrate()
