import psycopg2
from psycopg2._psycopg import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_connection():
    return psycopg2.connect(
        user="", #             <---- Enter your user( in database )
        password="",  #             <---- Enter your pass
        host="",  #             <---- Enter your host
        port="",  #             <---- Enter your port
        database= ""  #             <---- Enter your database
    )
def execute(query):
    connection = create_connection()
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        cursor.close()
        connection.close()
    except Error as e:
        print(e)
class DataBaseService:
    def __init__(self):
        self.create_table()


    @staticmethod
    def create_table():
        execute("CREATE TABLE IF NOT EXISTS todolist(title VARCHAR(40), deadline DATE, status BOOLEAN)")
    @staticmethod
    def insert_value(title,deadline,status):
        execute(f"INSERT INTO todolist VALUES {title,str(deadline), status}")
    @staticmethod
    def select_values(word):
        connection = create_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM todolist ORDER BY {word}")
            return cursor.fetchall()
        except Error as e:
            print(e)
        finally:
            if connection:
                connection.close()
    @staticmethod
    def update_value(title,deadline,status):
        execute(f"UPDATE todolist SET status = {status} WHERE title = '{title}' AND deadline = '{deadline}'")
    @staticmethod
    def delete_one(title,deadline):
        execute(f"DELETE FROM todolist WHERE title = '{title}' AND deadline = '{deadline}'")
    @staticmethod
    def delete_all():
        execute(f"DELETE FROM todolist")
