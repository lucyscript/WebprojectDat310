import sqlite3
from sqlite3 import Error

database = r"./Data/database.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

##### CREATE TABLES ######## 


sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                id TEXT UNIQUE NOT NULL,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL,
                                user_settings TEXT NOT NULL,
                                PRIMARY KEY(id)
                            );"""

sql_create_items_table = """CREATE TABLE IF NOT EXISTS items (
                                id INTEGER UNIQUE NOT NULL,
                                title TEXT NOT NULL,
                                description TEXT NOT NULL,
                                price REAL NOT NULL,
                                owner_id TEXT NOT NULL,
                                PRIMARY KEY(id),
                                FOREIGN KEY(owner_id) REFERENCES users(id)
                            );"""




def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

#### INSERT #########

def add_user(conn, id, username, password, user_settings = ""):
    """
    Add a new user into the users table
    :param conn:
    :param id:
    :param username:
    :param password:
    """
    sql = ''' INSERT INTO users(id, username, password, user_settings)
              VALUES(?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (id, username, password, user_settings))
        conn.commit()
    except Error as e:
        print(e)

def init_users(conn):
    init = [(111111,"Dany","1234"),
            (222222,"Sveinung","4321"),
            (333333,"Kongen","0000")]
    for u in init:
        add_user(conn, u[0], u[1], u[2])

def add_item(conn, id, title, description, price, owner_id):
    """
    Add a new item into the items table
    :param conn:
    :param id:
    :param title:
    :param description:
    :param price:
    :param owner_id:
    """
    sql = ''' INSERT INTO items(id, title, description, price, owner_id)
              VALUES(?,?,?,?,?) '''
    try:
        cur = conn.cursor()
        cur.execute(sql, (id, title, description, price, owner_id))
        conn.commit()
    except Error as e:
        print(e)

def init_items(conn):
    init = [(1, "Sofa", "En fin sofa", 1000, 111111),
            (2, "Stol", "En fin stol", 500, 222222),
            (3, "Bord", "Et fint bord", 2000, 333333)]
    for i in init:
        add_item(conn, i[0], i[1], i[2], i[3], i[4])

#### SETUP ####

def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_items_table)
        init_users(conn)
        init_items(conn)

        conn.close()


if __name__ == '__main__':
    # If executed as main, this will create tables and insert initial data
    setup()

