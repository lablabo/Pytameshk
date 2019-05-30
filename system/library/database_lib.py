import sqlite3
from sqlite3 import Error


class controller:

    def __init__(self, register):
        pass

    # create a database connection to a SQLite database
    def connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print("Database Error :: " + e)
            exit(1)
        # finally:
        #    conn.close()

    # create a database connection to a database that resides in the memory
    def memoryConnection(self):
        try:
            conn = sqlite3.connect(':memory:')
        except Error as e:
            print("Memory Database Error :: " + e)
        # finally:
        #    conn.close()

    # create a table from the create_table_sql statement
    # :param conn: Connection object
    # :param create_table_sql: a CREATE TABLE statement
    # :return:
    def createTable(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print("Create Table Error :: " + e)
            exit(1)

    # Create a new project into the projects table
    # :param conn:
    # :param project:
    # :return: project id
    def insert(self, conn, query, data):
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return cur.lastrowid

    # Select Records
    # :param conn: the Connection object
    # :param priority:
    # :return: array
    def select(self, conn, query, data):
        cur = conn.cursor()
        cur.execute(query, data)
        rows = cur.fetchall()

        result = []
        for row in rows:
            result.append(row)

        return result
